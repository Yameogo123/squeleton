
import { API_URL } from "@/assets/constantes/constante";


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
export async function Send(link:string, data:any, stringify:boolean=true, tok:string=""): Promise<object>{
    try {
        const headers: Record<string, string> = {
            authorization: "Bearer " + tok,
            ...(stringify && { 'Content-Type': 'application/json' })
        };

        const response = await fetch(API_URL + link, {
            method: 'POST',
            headers,
            body: stringify ? JSON.stringify(data) : data
        });
    
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
    
        return await response.json();
    } catch (error) {
        throw error; // Re-throw for calling code to handle
    }
}

/**
 * Sends a GET request to the specified link with optional authorization token.
 *
 * @param {string} link - The endpoint to send the GET request to.
 * @param {string} [tok=""] - The optional authorization token to include in the request headers.
 * @returns {Promise<Object>} - A promise that resolves to the JSON response from the server.
 */
export async function Get(link:string, tok:string=""):Promise<Object>{
    const options = {
        method: 'get',
        headers: {
            'Content-Type': 'application/json',
            authorization:"Bearer "+tok,
        }
    };
    const response = await fetch(API_URL+link, options);
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
export async function Update(link:string, data:any, tok: string="", stringify: boolean=true):Promise<Object>{
    let head : Record<string, string>={
        authorization:"Bearer "+tok,
    }
    if(stringify){
        head={
            'Content-Type': 'application/json',
            'authorization': "Bearer "+tok,
            'Accept': 'application/json',
        }
    }
    const options = {
        method: 'put',
        headers: head,
        body: stringify ? JSON.stringify(data) : data
    }; 
    const response = await fetch(API_URL+link, options);
    return response.json();
}

/**
 * Sends a DELETE request to the specified link with the provided token.
*
* @param {string} link - The endpoint to which the DELETE request is sent.
* @param {string} [tok=""] - The authorization token to be included in the request headers.
* @returns {Promise<Object>} - A promise that resolves to the JSON response from the server.
*/
export async function Remove(link:string, tok:string=""):Promise<Object>{ 
    const options = {
        method: 'delete',
        headers: {
            authorization:"Bearer "+tok,
        },
        Authorization:"Bearer "+tok,
    };
    const response = await fetch(API_URL+link, options);
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
export async function SendMessage(data:any):Promise<Object>{
    let head={
        'Content-Type' : 'application/json',
        //authorization:"Bearer "+tok,
    }
    const options = {
        method: 'post',
        headers: head,
        body: JSON.stringify(data),
        redirect: 'follow' as RequestRedirect
    };
    const response = await fetch("https://gateway.intechsms.sn/api/send-sms", options);
    return response.json();
}



export async function sendPushNotification(title:string = "Productivity", body: string = "That is a notification", expoPushToken: string) {
    const message = {
        to: expoPushToken, //"ExponentPushToken[xxxxxxxxxxxxxxxxxxxxxx]"
        sound: 'default',
        title: title,
        body: body,
        data: { someData: 'goes here' },
    };

    await fetch('https://exp.host/--/api/v2/push/send', {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Accept-encoding': 'gzip, deflate',
            'Content-Type': 'application/json',
            },
        body: JSON.stringify(message),
    });
}


