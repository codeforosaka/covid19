type DataType = {
  attr: '検査実施人数'
  value: number
  children: [
    {
      attr: '陽性患者数'
      value: number
      children: [
        {
          attr: '入院中'
          value: number
          children: [
            {
              attr: '軽症・中等症'
              value: number
            },
            {
              attr: '重症'
              value: number
            }
          ]
        },
        {
          attr: '退院'
          value: number
        },
        {
          attr: '死亡'
          value: number
        },
        {
          attr: '自宅療養'
          value: number
        },
        {
          attr: '宿泊療養'
          value: number
        },
        {
          attr: '療養等調整中'
          value: number
        },
        {
          attr: '入院調整中'
          value: number
          children: [
            {
              attr: '入院待機中'
              value: number
            },
            {
              attr: '入院もしくは療養方法の調整中'
              value: number
            }
          ]
        },
        {
          attr: '府外健康観察'
          value: number
        }
      ]
    }
  ]
}

type ConfirmedCasesType = {
  検査実施人数: number
  陽性物数: number
  入院中: number
  軽症中等症: number
  重症: number
  死亡: number
  退院: number
  現在陽性者数: number
  自宅療養: number
  宿泊療養: number
  療養等調整中: number
  入院調整中: number
  入院待機中: number
  入院もしくは療養方法の調整中: number
  府外健康観察: number
}

export default (data: DataType) => {
  const formattedData: ConfirmedCasesType = {
    検査実施人数: data.value,
    陽性物数: data.children[0].value,
    入院中: data.children[0].children[0].value,
    軽症中等症: data.children[0].children[0].children[0].value,
    重症: data.children[0].children[0].children[1].value,
    死亡: data.children[0].children[2].value,
    退院: data.children[0].children[1].value,
    現在陽性者数: 0,
    自宅療養: data.children[0].children[3].value,
    宿泊療養: data.children[0].children[4].value,
    療養等調整中: data.children[0].children[5].value,
    入院調整中: data.children[0].children[6].value,
    入院待機中: data.children[0].children[6].children[0].value,
    入院もしくは療養方法の調整中:
      data.children[0].children[6].children[1].value,
    府外健康観察: data.children[0].children[7].value
  }

  formattedData['現在陽性者数'] =
    formattedData['入院中'] +
    formattedData['入院調整中'] +
    formattedData['自宅療養'] +
    formattedData['宿泊療養'] +
    formattedData['療養等調整中']

  return formattedData
}
