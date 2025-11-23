const AUTH_KEY = 'health_authority_auth';
const CREDENTIALS = {
  email: 'health@authority.gov',
  password: 'admin123'
};

/**
 * Check if user is logged in
 */
export const isAuthenticated = () => {
  const auth = localStorage.getItem(AUTH_KEY);
  if (!auth) return false;
  
  try {
    const parsed = JSON.parse(auth);
    return parsed.loggedIn === true && parsed.email === CREDENTIALS.email;
  } catch {
    return false;
  }
};

/**
 * Login with credentials
 * @param {string} email
 * @param {string} password
 * @returns {boolean} Success status
 */
export const login = (email, password) => {
  if (email === CREDENTIALS.email && password === CREDENTIALS.password) {
    const authData = {
      loggedIn: true,
      email: email,
      timestamp: new Date().toISOString()
    };
    localStorage.setItem(AUTH_KEY, JSON.stringify(authData));
    return true;
  }
  return false;
};

/**
 * Logout user
 */
export const logout = () => {
  localStorage.removeItem(AUTH_KEY);
};

/**
 * Get current user email
 */
export const getCurrentUser = () => {
  const auth = localStorage.getItem(AUTH_KEY);
  if (!auth) return null;
  
  try {
    const parsed = JSON.parse(auth);
    return parsed.email;
  } catch {
    return null;
  }
};

