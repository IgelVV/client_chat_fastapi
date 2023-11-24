export const setObjectInLocalStorage = (key, value) => {
    localStorage.setItem(key, JSON.stringify(value));
};
  
export const getObjectFromLocalStorage = (key) => {
    const storedValue = localStorage.getItem(key);
    return storedValue ? JSON.parse(storedValue) : null;
};

export const updateOrCreateObjectInLocalStorage = (key, updatedValues) => {
    const storedObject = getObjectFromLocalStorage(key);
  
    const updatedObject = { ...storedObject, ...updatedValues };
  
    localStorage.setItem(key, JSON.stringify(updatedObject));
};
