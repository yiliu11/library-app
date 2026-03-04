import { IsInt, IsNotEmpty, IsEnum, IsString, IsOptional } from 'class-validator';
import { RequestStatus } from './request.dto';

export class RequestDecisionDTO {
  @IsInt()
  @IsNotEmpty()
  requestId: number;

  @IsEnum(RequestStatus)
  @IsNotEmpty()
  status: RequestStatus;

  @IsString()
  @IsOptional()
  notes?: string;
}
