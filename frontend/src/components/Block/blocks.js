const textBlock = {
  sequence_number: 0,
  type: 'text_block',
  message_text: ''
};

const imageBlock = {
  sequence_number: 0,
  type: 'image_block',
  image_path: ''
};

const questionBlock = {
  sequence_number: 0,
  type: 'question_block',
  answer_type: 'any',
  message_text: ''
};

const csvBlock =  {
  sequence_number: 0,
  type: 'csv_block',
  file_path: '',
  data: {}
};

const emailBlock = {
  sequence_number: 0,
  type: 'email_block',
  subject: '',
  text: '',
  recipient_email: ''
};

const apiBlock = {
  sequence_number: 0,
  type: 'api_block',
  url: '',
  http_method: 'GET',
  headers: {},
  body: {}
};

export default {
  textBlock,
  imageBlock,
  questionBlock,
  csvBlock,
  emailBlock,
  apiBlock
}