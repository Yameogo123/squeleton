import { images } from "@/assets/constantes/constante";
import { tacheType } from "@/assets/constantes/types";
import { useErrorToast, useWarningToast } from "@/hooks/useToast";
import moment from 'moment';
//import auth from '@react-native-firebase/auth';

/**
 * Updates the state with the value from the input event.
 *
 * @param {any} val - the val to put in the function.
 * @param {Function} setFunction - The state setter function to update the value.
 */
export function setInputedValue(val:any, setFunction:Function) {
    setFunction(val);
}

/**
 * Empties all fields by setting their values to an empty string.
 *
 * @param {Array<Function>} selectors - An array of state setter functions.
 */
export function emptyAllFields(selectors:Array<Function>) {
    selectors.forEach(input => {
        input("");
    });
}

/**
 * Gets the current year.
 *
 * @returns {number} The current year.
 */
export function getCurrentYear() {
    return new Date().getFullYear();
}

/**
 * Gets the current date in the format YYYY-MM-DD.
 *
 * @returns {string} The current date formatted as YYYY-MM-DD.
 */
export function getCurrentDate(){
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = String(currentDate.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
    const day = String(currentDate.getDate()).padStart(2, '0');

    const formattedDate = `${year}-${month}-${day}`;
    return formattedDate
}

/**
 * Validates if the given string is a valid email address.
 *
 * @param {string} email - The email address to validate.
 * @returns {boolean} True if the email is valid, false otherwise.
 */
export function isEmail(email:string):boolean {
    return /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/.test(email);
}

/**
 * Validates if the given string is a valid phone number.
 *
 * @param {string} phone - The phone number to validate.
 * @returns {boolean} True if the phone number is valid, false otherwise.
 */
export function isPhone(phone: string): boolean {
    const sanitizedPhone = phone.replace(/\s+/g, '');
    return /^\+?[0-9]{8,}$/.test(sanitizedPhone);
}

/**
 * Validates if the given string is a strong password.
 *
 * @param {string} password - The password to validate.
 * @returns {boolean} True if the password is strong, false otherwise.
 */
export function isPassword(password:string):boolean {
    return /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}$/.test(password);
}

/**
 * Validates if the given string is a valid name.
 *
 * @param {string} name - The name to validate.
 * @returns {boolean} True if the name is valid, false otherwise.
 */
export function isName(name:string):boolean {
    return /^[a-zA-Z\s.-]*$/.test(name);
}

/**
 * Generates a random number between 1 and 1000.
 *
 * @returns {number} A random number between 1 and 1000.
 */
export function generateRandomNumber() {
    return Math.floor(Math.random() * 1000) + 1;
}

/**
 * Removes special characters from a string, leaving only alphanumeric characters.
 *
 * @param {string} str - The string to process.
 * @returns {string} The string without special characters.
 */
export function removeSpecialCharacters(str:string):string {
    return str.replace(/[^a-zA-Z0-9]/g, '');
}

/**
 * Capitalizes the first character of a string.
 *
 * @param {string} str - The string to process.
 * @returns {string} The string with the first character capitalized.
 */
export function capitalizeFirstCharacter(str:string):string {
    if (!str) return ''; 
    return str.charAt(0).toUpperCase() + str.slice(1);
}


/**
 * Returns a random image from a predefined array of images
 * @function
 * @returns {string|Object} A randomly selected image from the images array
 * @example
 * const randomImage = returnRandomImg();
 */
export function returnRandomImg(): string{
    const randomIndex = Math.floor(Math.random() * images.length);
    return images[randomIndex]
}


export const truncateText = (text: string, maxLength: number = 20): string => {
  return text.length > maxLength ? text.substring(0, maxLength) + "..." : text;
};


export const calculateAge = (birthdate:string) => {
    // Parse the birthdate string (e.g., "1990-05-15")
    const birthDate = moment(birthdate, 'YYYY-MM-DD');
    
    // Get today's date
    const today = moment();
    
    // Calculate the difference in years
    const age = today.diff(birthDate, 'years');
    
    return age.toString();
};


export const validateAge = (birthdate:string) => {
    const age = moment().diff(birthdate, 'years');
    if (age < 15) useErrorToast("Vous devez avoir plus de 15 ans!");
    return age >= 15;
};




/**
 * Validates if the given date is not in the past.
 *
 * @param {string} date - The date to validate in the format YYYY-MM-DD.
 * @returns {boolean} True if the date is not in the past, false otherwise.
 */
export function isDateNotPassed(date: string, format: string = 'YYYY-MM-DD'): boolean {
    const inputDate = moment(date, format=format);
    
    const today = moment().startOf('day');
    return inputDate.isAfter(today);
}




// VerificationService.ts


export const sendVerificationCode = async (phoneNumber: string) => {
  try {
    
  } catch (error) {
    useWarningToast('Erreur envoi de code');
    throw error;
  }
};

export const confirmVerificationCode = async (
  confirmation: any, 
  code: string,
  userId: string
) => {
  try {
    
    
    return true;
  } catch (error) {
    useErrorToast('Erreur de confirmation de mot de passe.');
    throw error;
  }
};



export const formatDate = (date: Date) => {
    return date.toLocaleDateString('fr-FR');
};

export const formatTime = (date: Date) => {
    return date.toLocaleTimeString('fr-FR', {
        hour: '2-digit',
        minute: '2-digit'
    });
};


export const formatHMS = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    const padded = (num: number) => num.toString().padStart(2, '0');

    return `${padded(hours)}:${padded(mins)}:${padded(secs)}`;
};



// Helper to get start (Monday) and end (Sunday) of a week given an offset
export function getWeekRange(weekOffset = 0) {
    const today = new Date();
    const day = today.getDay(); // 0 (Sun) to 6 (Sat)
    const diffToMonday = ((day + 6) % 7); // Convert Sunday (0) to 6, Monday to 0, etc.

    const start = new Date(today);
    start.setDate(today.getDate() - diffToMonday + (weekOffset * 7));
    start.setHours(0, 0, 0, 0);

    const end = new Date(start);
    end.setDate(start.getDate() + 6);
    end.setHours(23, 59, 59, 999);

    const format = (date: Date) => 
        `${date.getDate().toString().padStart(2, '0')}-${(date.getMonth()+1).toString().padStart(2, '0')}-${date.getFullYear()}`;

    return { 
        start: format(start), 
        end: format(end) 
    };
}

