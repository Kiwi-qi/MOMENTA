import Vue from 'vue'
import Vuex from 'vuex'
import * as api from '../api/api'

Vue.use(Vuex);

export default new Vuex.Store({
    modules:{
        api
    }
});
