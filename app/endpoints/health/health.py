from fastapi import Depends
from injector import Injector

from app.endpoints.custom import Router
from app.endpoints.health.schema import HealthReport, HealthReportError
from app.interactors.health_check.interfaces import HealthCheckProbeInterface

router = Router(
    prefix="/health",
    tags=["health"],
)


@router.get("/", response_model=HealthReport | HealthReportError)
def get(injector: Injector = Depends(lambda: router.injector)) -> dict:
    health_check_probe = injector.get(HealthCheckProbeInterface)  # type: ignore[type-abstract]

    try:
        uptime = health_check_probe.get_uptime()
        cpu_usage = health_check_probe.get_cpu_usage()
        ram_usage = health_check_probe.get_ram_usage()

        return {
            "status": "healthy",
            "uptime": str(uptime),
            "cpu": cpu_usage,
            "ram": ram_usage,
        }

    except Exception as error:
        return {
            "status": "unhealthy",
            "error_type": error.__class__.__name__,
            "error": str(error),
        }
