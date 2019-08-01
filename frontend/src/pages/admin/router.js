import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: '/admin',
  routes: [
    // {
    //   path: '/admin/media',
    //   name: 'media',
    //   component: () => import('./views/Media.vue')
    // },
    {
      path: '/courses',
      name: 'courses',
      component: () => import('./views/Courses.vue')
    },
    {
      path: '/courses/:slug',
      name: 'coursesDetail',
      component: () => import('./views/CoursesDetail.vue')
    },
    {
      path: '/courses/:slug/lessons/:id',
      name: 'lessonsDetail',
      component: () => import('./views/LessonsDetail.vue')
    },
    {
      path: '/users',
      name: 'users',
      component: () => import('./views/Users.vue')
    },
  ],
})
