from pydantic import BaseModel


class CourseBlockReport(BaseModel):
    block_id: int
    block_title: str
    block_type: str
    is_default: bool


class CourseLessonReport(BaseModel):
    lesson_id: int
    lesson_name: str
    lesson_order: int
    blocks: list[CourseBlockReport]


class CourseModuleReport(BaseModel):
    module_id: int
    module_name: str
    module_order: int
    lessons: list[CourseLessonReport]


class CourseStructureReport(BaseModel):
    course_id: int
    course_name: str
    default_blocks: list[CourseBlockReport]
    modules: list[CourseModuleReport]
