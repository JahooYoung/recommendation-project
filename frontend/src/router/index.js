import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/movies',
    name: 'MovieList',
    component: () => import(/* webpackChunkName: "MovieList" */ '@/views/MovieList.vue')
  },
  {
    path: '/movies/:id',
    name: 'MovieDetail',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "MovieDetail" */ '@/views/MovieDetail.vue')
  },
  {
    path: '/rcmd-stats',
    name: 'RcmdStat',
    component: () => import(/* webpackChunkName: "RcmdStats" */ '@/views/RcmdStat.vue')
  },
  {
    path: '*',
    component: () => import(/* webpackChunkName: "NotFound" */ '@/views/NotFound.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
