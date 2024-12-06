from enum import Enum

FILE_EXTENSTIONS_MAPPING = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
    "bmp": "image/bmp",
    "webp": "image/webp",
    "svg": "image/svg+xml",
    "ico": "image/x-icon",
    "tiff": "image/tiff",
    "pdf": "application/pdf",
    "txt": "text/plain",
    "html": "text/html",
    "css": "text/css",
    "js": "application/javascript",
    "json": "application/json",
    "xml": "application/xml",
    "csv": "text/csv",
    "mp4": "video/mp4",
    "mov": "video/quicktime",
    "avi": "video/x-msvideo",
    "mp3": "audio/mpeg",
    "wav": "audio/wav",
    "ogg": "audio/ogg",
    "zip": "application/zip",
    "rar": "application/vnd.rar",
    "7z": "application/x-7z-compressed",
    "tar": "application/x-tar",
    "gz": "application/gzip",
    "doc": "application/msword",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "xls": "application/vnd.ms-excel",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "ppt": "application/vnd.ms-powerpoint",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}


class ProductType(Enum):
    COLLECT_EMAILS = "collect_emails"
    EXTERNAL_LINK = "external_link"
    VIDEO_EMBED = "video_embed"
    DIGITAL_DOWNLOAD = "digital_download"
    SESSION_BOOKING = "session_booking"
    WEBINAR = "webinar"
    E_COURSE = "e_course"
    FORM = "form"

    @staticmethod
    def is_collect_emails(product_details) -> bool:
        return product_details.get("product_type") == ProductType.COLLECT_EMAILS.value

    @staticmethod
    def is_external_link(product_details) -> bool:
        return product_details.get("product_type") == ProductType.EXTERNAL_LINK.value

    @staticmethod
    def is_video_embed(product_details) -> bool:
        return product_details.get("product_type") == ProductType.VIDEO_EMBED.value

    @staticmethod
    def is_digital_download(product_details) -> bool:
        return product_details.get("product_type") == ProductType.DIGITAL_DOWNLOAD.value

    @staticmethod
    def is_session_booking(product_details) -> bool:
        return product_details.get("product_type") == ProductType.SESSION_BOOKING.value

    @staticmethod
    def is_webinar(product_details) -> bool:
        return product_details.get("product_type") == ProductType.WEBINAR.value

    @staticmethod
    def is_e_course(product_details) -> bool:
        return product_details.get("product_type") == ProductType.E_COURSE.value

    @staticmethod
    def is_form(product_details) -> bool:
        return product_details.get("product_type") == ProductType.FORM.value
