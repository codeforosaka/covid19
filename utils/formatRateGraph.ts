import dayjs from 'dayjs'

type DataType = {
  date: Date
  denominator: number
  numerator: number
  rate: number
}

type GraphDataType = {
  updated: Date
  dateList: string[]
  denomList: number[]
  numerList: number[]
  rateList: number[]
}

export default (updated: Date, data: DataType[]) => {
  const today = new Date()
  const dateList: string[] = []
  const denomList: number[] = []
  const numerList: number[] = []
  const rateList: number[] = []
  data
    .filter(d => new Date(d.date) < today)
    .forEach(d => {
      const date = new Date(d.date)
      dateList.push(dayjs(date).format('YYYY-MM-DD'))
      denomList.push(d.denominator)
      numerList.push(d.numerator)
      rateList.push(d.rate)
    })

  const graphData: GraphDataType = {
    updated,
    dateList,
    denomList,
    numerList,
    rateList
  }
  return graphData
}
