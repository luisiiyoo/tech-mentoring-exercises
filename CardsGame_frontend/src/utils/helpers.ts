export const timestampToDateStr = (timestamp: number): string => {
  return new Date(timestamp * 1000).toDateString()
}

export const sortNumber = (a: number, b: number, ascending: boolean): number => {
  if (ascending) return a - b
  return b - a
}
