


const state = "{{cookiecutter.project_slug}}_state"

/**
 * Loads the state from localStorage.
 *
 * @returns {Object|undefined} The parsed state object if it exists and is valid JSON, otherwise undefined.
 */
export const loadState = () => {
    if(localStorage.length ===0) return undefined
    try {
        const serializedState = localStorage.getItem(state);
        if (serializedState === null) {
            return undefined;
        }
        return JSON.parse(serializedState);
    } catch (err) {
        return undefined;
    }
}; 

/**
 * Saves the given state to localStorage.
 *
 * @param {Object} state - The state object to be saved.
 * @throws Will ignore any errors that occur during the serialization or saving process.
 */
export const saveState = (st) => {
    try {
        const serializedState = JSON.stringify(st);
        localStorage.setItem(state, serializedState);
    } catch {
      // ignore write errors
    }
};

/**
 * Removes all items from the local storage.
 * This function clears the entire local storage, removing all key-value pairs.
 */
export const removeAll= ()=>{
    localStorage.clear();
}