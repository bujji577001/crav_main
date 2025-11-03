/*
* I've updated this file to use localStorage.
* This will keep your user logged in even if they refresh the page.
*
* 1. It loads the user and token from localStorage when the app starts.
* 2. The 'login' action saves the user and token to localStorage.
* 3. The 'logout' action removes the user and token from localStorage.
*/
const store = new Vuex.Store({
    state: {
        // Try to load token and user from localStorage on initial load
        token: localStorage.getItem('token') || null,
        user: JSON.parse(localStorage.getItem('user')) || null,
        cart: [],
    },
    mutations: {
        SET_TOKEN(state, token) {
            state.token = token;
        },
        SET_USER(state, user) {
            state.user = user;
        },
        CLEAR_AUTH(state) {
            state.token = null;
            state.user = null;
        },
        // (Your cart mutations remain unchanged)
    },
    actions: {
        async login({ commit }, { email, password }) {
            // The login action is special, it uses fetch directly
            // because it's the only one that *gets* a token.
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Login failed.');
            }

            // Save to localStorage
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));

            // Save to Vuex state
            commit('SET_TOKEN', data.token);
            commit('SET_USER', data.user);
        },
        logout({ commit }) {
            // Clear from localStorage
            localStorage.removeItem('token');
            localStorage.removeItem('user');

            // Clear from Vuex state
            commit('CLEAR_AUTH');
            // (You might want to clear cart here too)
        },
        // (Your cart actions remain unchanged)
    },
    getters: {
        isAuthenticated: (state) => !!state.token,
        currentUser: (state) => state.user,
        userRoles: (state) => state.user ? state.user.roles : [],
        // (Your cart getters remain unchanged)
    },
});

export default store;
