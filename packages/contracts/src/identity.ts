import type { ISODateTime } from "./common.js";

export type OrgRole = "owner" | "member" | "service_account";

export type ActorContext = {
  actorId: string;
  orgId: string;
  role: OrgRole;
};

export type UserSummary = {
  id: string;
  email: string;
  displayName: string;
  createdAt: ISODateTime;
};

export type OrgSummary = {
  id: string;
  name: string;
  createdAt: ISODateTime;
};
