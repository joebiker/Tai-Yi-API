import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from enum import Enum

router = APIRouter(prefix="/calculator", tags=["Calculator"])
logger = logging.getLogger(__name__)


class Operation(str, Enum):
    add = "add"
    subtract = "subtract"
    multiply = "multiply"
    divide = "divide"


class CalculatorRequest(BaseModel):
    a: float
    b: float
    operation: Operation


class CalculatorResponse(BaseModel):
    a: float
    b: float
    operation: Operation
    result: float


def _compute(a: float, b: float, operation: Operation) -> float:
    """Pure helper — performs the arithmetic and returns the result."""
    match operation:
        case Operation.add:
            return a + b
        case Operation.subtract:
            return a - b
        case Operation.multiply:
            return a * b
        case Operation.divide:
            if b == 0:
                raise HTTPException(status_code=400, detail="Division by zero is not allowed.")
            return a / b
        case _:
            raise HTTPException(status_code=400, detail=f"Unknown operation: {operation}")


@router.post("", response_model=CalculatorResponse, summary="Perform a calculation")
async def calculate(payload: CalculatorRequest):
    """
    Perform a basic arithmetic operation on two numbers.

    - **add** – a + b
    - **subtract** – a - b
    - **multiply** – a × b
    - **divide** – a ÷ b  *(b must not be zero)*
    """
    result = _compute(payload.a, payload.b, payload.operation)
    logger.info(
        "Calculator (POST): %s %s %s = %s",
        payload.a,
        payload.operation.value,
        payload.b,
        result,
        extra={
            "endpoint": "calculate",
            "operation": payload.operation.value,
            "a": payload.a,
            "b": payload.b,
            "result": result,
        },
    )
    return CalculatorResponse(a=payload.a, b=payload.b, operation=payload.operation, result=result)


@router.get(
    "/{operation}",
    response_model=CalculatorResponse,
    summary="Perform a calculation via query params",
)
async def calculate_via_query(operation: Operation, a: float, b: float):
    """
    Convenience GET endpoint — supply **a**, **b** and the **operation** in the URL.

    Example: `/calculator/add?a=5&b=3`
    """
    result = _compute(a, b, operation)
    logger.info(
        "Calculator (GET): %s %s %s = %s",
        a,
        operation.value,
        b,
        result,
        extra={
            "endpoint": "calculate_via_query",
            "operation": operation.value,
            "a": a,
            "b": b,
            "result": result,
        },
    )
    return CalculatorResponse(a=a, b=b, operation=operation, result=result)
