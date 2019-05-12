<template>
  <el-container>
    <el-header height="61">
      <NavBar
        active-index="admin"
        :lock-login-dialog="true"
      />
    </el-header>
    <el-container v-if="$store.state.userInfo !== null && $store.state.userInfo['is_logged_in'] === true">
      <el-aside>
        <el-menu />
      </el-aside>
      <el-container>
        <transition>
          <router-view />
        </transition>
      </el-container>
    </el-container>
  </el-container>
</template>

<script>
import NavBar from '../../components/NavBar.vue'
import LoginBox from '../../components/LoginBox'

export default {
  name: 'App',
  components: {
    NavBar,
    LoginBox,
  }
}
</script>

<style>
  html, body {
    padding: 0;
    margin: 0;
  }

  #nprogress .spinner {
    top: 76px;
  }
</style>
