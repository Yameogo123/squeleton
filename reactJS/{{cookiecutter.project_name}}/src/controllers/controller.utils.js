

/**
 * Updates the state with the value from the input event.
 *
 * @param {Event} e - The input event.
 * @param {Function} setFunction - The state setter function to update the value.
 */
export function getInputedValue(e, setFunction) {
    setFunction(e.target.value);
}

/**
 * Empties all fields by setting their values to an empty string.
 *
 * @param {Array<Function>} selectors - An array of state setter functions.
 */
export function emptyAllFields(selectors) {
    selectors.forEach(input => {
        input("");
    });
}

/**
 * Reloads the current page.
 */
export const reloadPage = () => {
    window.location.reload();
};

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
export function isEmail(email) {
    return /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/.test(email);
}

/**
 * Validates if the given string is a valid phone number.
 *
 * @param {string} phone - The phone number to validate.
 * @returns {boolean} True if the phone number is valid, false otherwise.
 */
export function isPhone(phone) {
    return /^[0-9]{8,}$/.test(phone);
}

/**
 * Validates if the given string is a strong password.
 *
 * @param {string} password - The password to validate.
 * @returns {boolean} True if the password is strong, false otherwise.
 */
export function isPassword(password) {
    return /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}$/.test(password);
}

/**
 * Validates if the given string is a valid name.
 *
 * @param {string} name - The name to validate.
 * @returns {boolean} True if the name is valid, false otherwise.
 */
export function isName(name) {
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
export function removeSpecialCharacters(str) {
    return str.replace(/[^a-zA-Z0-9]/g, '');
}

/**
 * Capitalizes the first character of a string.
 *
 * @param {string} str - The string to process.
 * @returns {string} The string with the first character capitalized.
 */
export function capitalizeFirstCharacter(str) {
    if (!str) return ''; 
    return str.charAt(0).toUpperCase() + str.slice(1);
}


export const images = [
    "https://static.vecteezy.com/ti/vecteur-libre/p1/8169402-formes-abstraites-et-lignes-dans-les-couleurs-pastel-nudes-fond-neutre-dans-le-style-minimaliste-contemporain-illustrationle-gratuit-vectoriel.jpg",
    "https://img.freepik.com/vecteurs-premium/modele-fond-motif-couleur-neutre_656853-281.jpg",
    "https://img.freepik.com/vecteurs-premium/fond-illustration-dessine-main-formes-abstraites-illustration-vectorielle_656853-671.jpg"
]

/**
 * Returns a random image from a predefined array of images
 * @function
 * @returns {string|Object} A randomly selected image from the images array
 * @example
 * const randomImage = returnRandomImg();
 */
export function returnRandomImg(){
    const randomIndex = Math.floor(Math.random() * images.length);
    return images[randomIndex]
}


