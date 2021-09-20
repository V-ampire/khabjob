export function convertToISODateString(date) {
  /**
   * FIXES problem with datepicker that toISOString returns day - 1
   * 
   * @date Date object
   */
  const year = date.getFullYear().toString()
  const month = (date.getMonth() + 1).toString()
  const fullMonth = (month.length > 1) ? month : '0' + month
  const day = date.getDate().toString()
  const fullDay = (day.length > 1) ? day : '0' + day

  return `${year}-${fullMonth}-${fullDay}`
}

export function getTodayDate() {
  const today = new Date()
  return today.toISOString().split("T")[0]
}