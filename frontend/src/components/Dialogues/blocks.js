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

export default {
  textBlock,
  questionBlock,
  csvBlock,
}