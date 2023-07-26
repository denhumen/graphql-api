from graphene import String, ObjectType, Int

class CourseType(ObjectType):
  id = Int(required=True)
  title = String(required=True)
  instructor = String(required=True)
  description = String(required=True)
  rate = Int(required=True)
  publish_date = String()