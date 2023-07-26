from fastapi import FastAPI
import graphene
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from schemas import CourseType
import json

class Query (graphene.ObjectType):
  course_list = None
  get_course = graphene.List(CourseType)
  async def resolve_get_course(self, info):
    with open("./courses.json") as courses:
      course_list = json.load(courses)
    return course_list

class CreateCourse (graphene.Mutation):
    course = graphene.Field(CourseType)
    success = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String(required=True)
        instructor = graphene.String(required=True)
        description = graphene.String(required=True)
        rate = graphene.Int(required=True)

    async def mutate(self, info, id, title, instructor, description, rate):
        with open("./courses.json", "r+") as courses:
            course_list = json.load(courses)

            for course in course_list:
              if course['id'] == id:
                return CreateCourse(course=None, success=False)

            course_list.append({"id": id,
                                "title": title,
                                "instructor": instructor,
                                "description": description,
                                "rate": rate,
                                "publish_date": "12th May 2020"})
            courses.seek(0)
            json.dump(course_list, courses, indent=2)
        return CreateCourse(course=course_list[-1], success=True)

class DeleteCourse(graphene.Mutation):
    course = graphene.Field(CourseType)
    success = graphene.Boolean()

    class Arguments:
      id = graphene.Int(required=True)
    
    async def mutate(self, info, id):
        with open("./courses.json", "r+") as courses:
            course_list = json.load(courses)
        courseId = None
        for idx, course in enumerate(course_list):
          print(idx, course['id'], id, course['id'] == id)
          if course['id'] == id:
              courseId = idx
        print("courseId", courseId)
        if courseId is not None:
          deletedCourse = course_list.pop(courseId)
        else:
            return DeleteCourse(course = None, success=False)
        with open("./courses.json", "w") as courses:
          courses.seek(0)
          json.dump(course_list, courses, indent=2)
        return DeleteCourse(course=deletedCourse, success=True)

class Mutation(graphene.ObjectType):
  create_course = CreateCourse.Field()
  delete_course = DeleteCourse.Field()

app = FastAPI()

app.mount('/', GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutation), on_get=make_graphiql_handler()))