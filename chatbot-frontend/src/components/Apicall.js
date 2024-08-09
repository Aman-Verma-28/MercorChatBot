import axios from 'axios';

const sendMessageToApi = async (message) => {
  try {
    // Replace 'https://your-api-endpoint.com/message' with your actual API endpoint
    const response = await axios.post('http://15.207.230.178/chatbot/get-response/', {
        
            "query": "I want to hire someone with experience in Python and Node. My budget is $10000 a month",
            "chat_id": "e551fc88-4a14-4edf-a7bc-81d40bf74654"
        
    });

    // Assuming the API returns a JSON object with a 'message' field
    return response;
  } catch (error) {
    console.error("Error in sendMessageToApi:", error);
    throw error;
  }
};

export default sendMessageToApi;
