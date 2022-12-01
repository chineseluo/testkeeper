import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
//import Home from '../views/Home.vue'Vue.use(VueRouter)const routes = [{path: '/',name: 'Home',component: Home},{path: '/about',name: 'About',component: () => import('../views/About.vue')},{path: '*', // * 为通配符，表示其他路径都显示 404 页面component: () => import('../views/NotFound.vue')}
const routes = [
    {
        path: '/',
        name: 'home',
        component: HomeView
    },
    {
        path: '/about',
        name: 'about',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
    }
    ,
    {
        path: "/:catchAll(.*)", // * 为通配符，表示其他路径都显示 404 页面
        // name: 'notfound',
        component: () => import('../views/NotFound.vue')
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router
