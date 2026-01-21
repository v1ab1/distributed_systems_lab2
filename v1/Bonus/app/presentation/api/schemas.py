from pydantic import Field, BaseModel, ConfigDict, constr


class PrivilegeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: constr(min_length=1, max_length=80)  # type: ignore
    status: constr(min_length=1, max_length=80) = Field(default="BRONZE")  # type: ignore
    balance: int | None = None


class SetBalanceRequest(BaseModel):
    balance: int
