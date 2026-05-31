from pydantic import BaseModel


class MdtReportRowSchema(BaseModel):
    student_name: str
    certificate_type: str
    status: str  # Descargado o No visto (Nel)
    viewed_at: str  # Fecha formateada o "—"


class MdtReportResponseSchema(BaseModel):
    course_id: int
    course_name: str
    certificate_type: str
    rows: list[MdtReportRowSchema]
