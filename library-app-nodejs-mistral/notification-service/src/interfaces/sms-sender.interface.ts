export interface ISmsSender {
  send(to: string, message: string): Promise<boolean>;
}
