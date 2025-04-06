


export const API= "http://localhost:8000" 

//"http://localhost:3002" //

/**
 * Sends a POST request to the specified endpoint
 * 
 * @async
 * @param {string} link - The API endpoint path to send the request to
 * @param {Object|FormData} data - The data to send in the request body
 * @param {boolean} [stringify=true] - Whether to stringify the data (true for JSON, false for FormData)
 * @param {string} [tok=""] - Bearer token for authorization
 * @returns {Promise<Object>} The parsed JSON response from the API
 * 
 * @throws {Error} If the network request fails
 * 
 * @example
 * // Send JSON data
 * await Send('/users', { name: 'John' }, true, 'auth-token');
 * 
 * // Send FormData
 * const formData = new FormData();
 * await Send('/upload', formData, false, 'auth-token');
 */
export async function Send(link, data, stringify=true, tok=""){
    let head={
        //'Content-Type': 'multipart/form-data',
        authorization:"Bearer "+tok,
    }
    if(stringify){
        head={
            'Content-Type' : 'application/json',
            "authorization"  : "Bearer "+tok,
        }
    }
    const options = {
        method: 'post',
        headers: head,
        body: stringify ? JSON.stringify(data) : data
    };
    const response = await fetch(API+link, options);
    return response.json();
}

/**
 * Sends a GET request to the specified link with optional authorization token.
 *
 * @param {string} link - The endpoint to send the GET request to.
 * @param {string} [tok=""] - The optional authorization token to include in the request headers.
 * @returns {Promise<Object>} - A promise that resolves to the JSON response from the server.
 */
export async function Get(link, tok=""){
    const options = {
        method: 'get',
        headers: {
            'Content-Type': 'application/json',
            authorization:"Bearer "+tok,
        }
    };
    const response = await fetch(API+link, options);
    //if(response.statusText=== "Unauthorized") window.location.reload()
    return response.json();
}

/**
 * Updates a resource at the specified link with the provided data.
 *
 * @param {string} link - The endpoint to which the request is sent.
 * @param {Object} data - The data to be sent in the request body.
 * @param {string} [tok=""] - The authorization token to be included in the request headers.
 * @param {boolean} [stringify=true] - Whether to stringify the data before sending it.
 * @returns {Promise<Object>} - A promise that resolves to the response data in JSON format.
 */
export async function Update(link, data, tok="", stringify=true){
    let head={
        //'Content-Type': 'application/json',
        authorization:"Bearer "+tok,
    }
    if(stringify){
        head={
            'Content-Type': 'application/json',
            authorization: "Bearer "+tok,
            'Accept': 'application/json',
        }
    }
    const options = {
        method: 'put',
        headers: head,
        body: stringify ? JSON.stringify(data) : data
    }; 
    const response = await fetch(API+link, options);
    return response.json();
}

/**
 * Sends a DELETE request to the specified link with the provided token.
*
* @param {string} link - The endpoint to which the DELETE request is sent.
* @param {string} [tok=""] - The authorization token to be included in the request headers.
* @returns {Promise<Object>} - A promise that resolves to the JSON response from the server.
*/
export async function Remove(link, tok=""){ 
    const options = {
        method: 'delete',
        headers: {
            //'Content-Type': 'application/json',
            authorization:"Bearer "+tok,
        },
        Authorization:"Bearer "+tok,
    };
    const response = await fetch(API+link, options);
    return response.json();
}


/**
 * Sends an SMS message through the IntechSMS API
 * @async
 * @param {Object} data - The message data to be sent
 * @param {string} data.message - The SMS message content
 * @param {string} data.to - The recipient phone number
 * @returns {Promise<Object>} The API response data
 * @throws {Error} If the network request fails
 * @example
 * const data = {
 *   message: "Hello World",
 *   to: "+221XXXXXXXXX"
 * };
 * const response = await SendMessage(data);
 */
export async function SendMessage(data){
    let head={
        'Content-Type' : 'application/json',
        //authorization:"Bearer "+tok,
    }
    const options = {
        method: 'post',
        headers: head,
        body: JSON.stringify(data),
        redirect: 'follow'
    };
    const response = await fetch("https://gateway.intechsms.sn/api/send-sms", options);
    return response.json();
}




