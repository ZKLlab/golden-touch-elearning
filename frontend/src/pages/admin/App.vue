<template>
  <el-container>
    <el-header height="61">
      <NavBar
        active-index="admin"
        :lock-login-dialog="true"
      />
    </el-header>
    <el-container
      v-if="$store.state.userInfo !== null && $store.state.userInfo['is_logged_in'] === true"
      class="main-container"
    >
      <el-aside>
        <el-menu
          class="aside-menu"
          :default-active="$route.path.split('/').slice(0, 2).join('/')"
          :router="true"
        >
          <el-menu-item
            class="menu-item"
            index="/"
          >
            <font-awesome-icon
              class="menu-item-icon"
              icon="home"
            />
            首页
          </el-menu-item>
          <el-menu-item
            class="menu-item"
            index="/courses"
          >
            <font-awesome-icon
              class="menu-item-icon"
              icon="book"
            />
            课程管理
          </el-menu-item>
          <el-menu-item
            class="menu-item"
            index="/users"
          >
            <font-awesome-icon
              class="menu-item-icon"
              icon="users"
            />
            用户管理
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <!--        <transition name="el-fade-in">-->
        <router-view />
        <!--        </transition>-->
      </el-container>
    </el-container>
  </el-container>
</template>

<script>
import NavBar from '../../components/NavBar'

export default {
  name: 'App',
  components: {
    NavBar,
  },
}
</script>

<style>
  html, body {
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
    font-size: 14px;
    padding: 0;
    margin: 0;
    min-width: 960px;
  }

  .main-container {
    min-height: calc(100vh - 61px);
  }

  .aside-menu {
    min-height: 100%;
  }

  .aside-menu .menu-item {
    font-size: 14px !important;
  }

  .aside-menu .menu-item.is-active {
    background: transparent;
  }

  .menu-item-icon {
    font-size: 16px !important;
    width: 1em !important;
    position: relative;
    top: -1px;
    margin-left: 20px;
    margin-right: 6px;
  }

  #nprogress .spinner {
    top: 76px;
  }
</style>
