const textBlock = {
  sequence_number: 0,
  type: 'text_block',
  message_text: ''
};

const questionBlock = {
  sequence_number: 0,
  type: 'question_block',
  answer_type: 'any',
  message_text: ''
}

const csvBlock =  {
  sequence_number: 0,
  type: 'csv_block',
  file_path: '',
  data: {}
}

const emailBlock = {
  sequence_number: 0,
  type: 'email_block',
  subject: '',
  text: '',
  recipient_email: ''
}

export default {
  textBlock,
  questionBlock,
  csvBlock,
  emailBlock,
}