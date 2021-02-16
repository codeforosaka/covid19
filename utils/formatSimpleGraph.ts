import dayjs from 'dayjs'

type DataType = {
  date: Date
  value: number
}

type GraphDataType = {
  updated: Date
  dateList: string[]
  valList: number[]
}

export default (updated: Date, data: DataType[]) => {
  const today = new Date()
  const dateList: string[] = []
  const valList: number[] = []
  data
    .filter(d => new Date(d.date) < today)
    .forEach(d => {
      const date = new Date(d.date)
      dateList.push(dayjs(date).format('YYYY-MM-DD'))
      valList.push(d.value)
    })

  const graphData: GraphDataType = {
    updated,
    dateList,
    valList
  }
  return graphData
}
