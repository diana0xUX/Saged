// Saged Members — Google Apps Script webhook
// Deploy as Web App: Execute as Me, Anyone can access
// Receives form submissions and creates records in Notion

var NOTION_TOKEN = 'ntn_y99247585507sGyc8qmVpYCw5LwVWgpX8jgGOTFflPEb4J'
var DATABASE_ID  = '3ff24f8f-cc16-81cd-88e7-e6d3a14d28cc'

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents)

    var payload = {
      parent: { database_id: DATABASE_ID },
      properties: {
        'Имя':           { title:        [{ text: { content: data.name    || '' } }] },
        'Email':         { email:        data.email   || null },
        'Телефон':       { phone_number: data.phone   || null },
        'NIE / Паспорт': { rich_text:    [{ text: { content: data.nie     || '' } }] },
        'Адрес':         { rich_text:    [{ text: { content: data.address || '' } }] },
        'Тип участия':   { select:       { name: data.typeName || '' } },
        'Статус':        { select:       { name: 'Новая' } },
        'Дата заявки':   { date:         { start: new Date().toISOString().split('T')[0] } }
      }
    }

    if (data.dob) {
      payload.properties['Дата рождения'] = { date: { start: data.dob } }
    }

    UrlFetchApp.fetch('https://api.notion.com/v1/pages', {
      method: 'post',
      headers: {
        'Authorization':  'Bearer ' + NOTION_TOKEN,
        'Content-Type':   'application/json',
        'Notion-Version': '2022-06-28'
      },
      payload:            JSON.stringify(payload),
      muteHttpExceptions: true
    })
  } catch(err) {
    Logger.log('Error: ' + err.toString())
  }

  return ContentService
    .createTextOutput(JSON.stringify({ ok: true }))
    .setMimeType(ContentService.MimeType.JSON)
}

function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify({ ok: true, service: 'Saged Members' }))
    .setMimeType(ContentService.MimeType.JSON)
}
