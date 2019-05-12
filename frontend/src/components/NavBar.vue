<template>
  <div>
    <el-menu
      ref="menu"
      mode="horizontal"
      background-color="#FAFAFA"
      unique-opened
      :default-active="activeIndex"
      @select="select"
    >
      <li
        ref="brand"
        class="menu-brand"
      >
        （Logo预留位）
      </li>
      <template v-if="$store.state.userInfo !== null">
        <el-menu-item
          v-if="!lockLoginDialog && !$store.state.userInfo['is_logged_in']"
          class="menu-right"
          index="login"
          @click="loginDialogVisible = true"
        >
          登录
        </el-menu-item>
        <template v-if="$store.state.userInfo['is_logged_in']">
          <el-submenu
            class="menu-right"
            index="user"
          >
            <template slot="title">
              <font-awesome-icon
                v-if="$store.state.userInfo['user_type'] === 0"
                class="menu-icon-user"
                icon="user-circle"
              />
              <font-awesome-icon
                v-if="$store.state.userInfo['user_type'] === 1"
                class="menu-icon-user"
                icon="chalkboard-teacher"
              />
              <font-awesome-icon
                v-if="$store.state.userInfo['user_type'] === 2"
                class="menu-icon-user"
                icon="drafting-compass"
              />
              <div class="logged-in-user">
                {{ $store.state.userInfo['display_name'] }}<br>
                <small>{{ userType }}
                  <template v-if="$store.state.userInfo['is_superuser']">
                    超级用户
                  </template>
                </small>
              </div>
            </template>
            <el-menu-item index="user-modify">
              <font-awesome-icon
                class="menu-icon-prefix"
                icon="key"
              />
              修改密码
            </el-menu-item>
            <el-menu-item
              index="user-logout"
              @click="logout"
            >
              <font-awesome-icon
                class="menu-icon-prefix"
                icon="sign-out-alt"
              />
              退出登录
            </el-menu-item>
          </el-submenu>
        </template>
        <el-menu-item
          v-if="$store.state.userInfo['userType'] === 2"
          class="menu-right"
          index="admin"
        >
          <a :href="activeIndex === 'admin' ? 'javascript:void(0)' : '/admin'">平台管理</a>
        </el-menu-item>
      </template>
    </el-menu>
    <el-dialog
      title="登录"
      :visible.sync="loginDialogVisible"
      width="360px"
      :close-on-click-modal="!lockLoginDialog"
      :close-on-press-escape="!lockLoginDialog"
      :show-close="!lockLoginDialog"
      center
      append-to-body
    >
      <LoginBox @login-success="loginDialogVisible = false" />
    </el-dialog>
  </div>
</template>

<script>
import '../plugins/element.js'
import '../plugins/fontawesome.js'
import axios from 'axios'
import LoginBox from "./LoginBox"

export default {
  name: 'NavBar',
  components: {LoginBox},
  props: {
    activeIndex: {
      type: String,
      default: null,
    },
    lockLoginDialog: {
      type: Boolean,
    }
  },
  data() {
    return {
      loginDialogVisible: false,
      loggingOut: false
    }
  },
  computed: {
    userType() {
      return {0: '学生', 1: '学校', 2: '志愿者'}[this.$store.state.userInfo['user_type']]
    },
    userInfo() {
      return this.$store.state.userInfo
    },
  },
  watch: {
    userInfo() {
      if (this.lockLoginDialog && this.$store.state.userInfo !== null) {
        if (!this.$store.state.userInfo['is_logged_in']) {
          this.loginDialogVisible = true
        }
      }
    }
  },
  mounted() {
    this.$refs['brand'].removeAttribute('tabindex')
    this.$store.dispatch('updateUserInfo')
  },
  methods: {
    select() {
      this.$refs['menu'].activeIndex = this.$props.activeIndex
    },
    logout() {
      const loading = this.$loading({
        lock: true,
        text: '正在退出登录',
      })
      axios.delete('/api/account/session').then(() => {
        this.$message.success('已退出登录！')
        this.$store.dispatch('updateUserInfo')
      }).catch(() => {
        this.$message.error('退出登录失败，请检查网络后重试！')
      }).then(() => {
        loading.close()
      })
    }
  }
}
</script>

<style>
  a {
    text-decoration: none;
  }

  .el-menu.el-menu--horizontal {
    margin-left: -20px;
    margin-right: -20px;
    padding-left: 20px;
    padding-right: 20px;
    font-size: 16px;
  }

  .el-menu-item > a {
    vertical-align: baseline;
  }

  .menu-brand {
    float: left;
    height: 60px;
    line-height: 60px;
    margin: 0;
    border: none;
    border-bottom: 2px solid transparent;
    font-size: 18px;
    color: #303133;
    padding: 0 20px;
    position: relative;
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
    white-space: nowrap;
  }

  .menu-right {
    float: right !important;
  }

  .el-submenu__title, .el-menu-item {
    font-size: 16px;
  }

  .el-menu--horizontal > .el-menu.el-menu--popup > .el-menu-item {
    font-size: 14px;
  }

  .menu-icon-prefix {
    margin-left: 0.25em;
    margin-right: 0.5em;
    position: relative;
    top: -1px;
  }

  .menu-icon-user {
    margin-right: 0.5em;
    position: relative;
    top: -1px;
    font-size: 24px;
  }

  .logged-in-user {
    display: inline-block;
    line-height: 1;
  }

  .logged-in-user > small {
    font-size: 12px;
  }
</style>