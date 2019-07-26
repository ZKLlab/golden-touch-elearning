<template>
  <el-main>
    <el-tabs
      v-model="activeTab"
      @tab-click="refreshData"
    >
      <el-tab-pane
        label="志愿者"
        name="volunteer"
      />
      <el-tab-pane
        label="学校"
        name="school"
      />
      <el-tab-pane
        label="学生"
        name="student"
      />
    </el-tabs>
    <div v-if="tableSelection.length === 0">
      <el-button
        type="primary"
        size="small"
        @click="showProfile(null)"
      >
        <font-awesome-icon icon="user-plus" />
        添加{{ userType }}用户
      </el-button>
      <el-button
        size="small"
        plain
        :disabled="loading"
        @click="pullData"
      >
        <font-awesome-icon icon="sync-alt" />
        刷新
      </el-button>
    </div>
    <div v-if="tableSelection.length > 0">
      <el-button
        size="small"
        type="warning"
        plain
        :disabled="loading"
        @click="resetPasswords"
      >
        <font-awesome-icon icon="key" />
        重置密码
      </el-button>
    </div>
    <el-table
      v-loading="loading"
      :data="tableData"
      @selection-change="handleSelection"
    >
      <template slot="empty">
        <template v-if="!loading">
          没有符合条件的记录
        </template>
        <template v-else>
          &nbsp;
        </template>
      </template>
      <el-table-column
        type="selection"
        width="48"
        :selectable="rowSelectable"
      />
      <el-table-column
        prop="display_name"
        :label="displayNameLabel"
      >
        <template v-slot="scope">
          {{ scope['row']['display_name'] }}
          <font-awesome-icon
            v-if="scope['row']['gender'] === 1"
            class="gender-icon"
            icon="venus"
            style="color: #F48FB1"
          />
          <font-awesome-icon
            v-if="scope['row']['gender'] === 2"
            class="gender-icon"
            icon="mars"
            style="color: #64B5F6"
          />
        </template>
      </el-table-column>
      <el-table-column
        prop="username"
        label="用户名"
      >
        <template v-slot="scope">
          {{ scope['row']['username'] }}
          <el-tooltip
            v-if="scope['row']['is_current_user']"
            effect="dark"
            content="当前登录用户"
            :enterable="false"
            placement="top"
          >
            <font-awesome-icon
              class="cell-icon"
              icon="user"
            />
          </el-tooltip>
          <el-tooltip
            v-if="!scope['row']['has_password']"
            effect="dark"
            content="无登录密码"
            :enterable="false"
            placement="top"
          >
            <font-awesome-icon
              class="cell-icon"
              icon="asterisk"
            />
          </el-tooltip>
          <el-tooltip
            v-if="scope['row']['is_superuser']"
            effect="dark"
            content="超级用户"
            :enterable="false"
            placement="top"
          >
            <font-awesome-icon
              class="cell-icon"
              icon="crown"
            />
          </el-tooltip>
          <el-tooltip
            v-if="!scope['row']['is_active']"
            effect="dark"
            content="已停用"
            :enterable="false"
            placement="top"
          >
            <font-awesome-icon
              class="cell-icon"
              icon="lock"
            />
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column
        prop="last_login"
        label="上次登录"
        show-overflow-tooltip
      />
      <el-table-column
        key="actions"
        align="right"
      >
        <template v-slot="scope">
          <el-button
            class="actions-button"
            type="text"
            size="small"
            @click="showProfile(scope['row'])"
          >
            修改
          </el-button>
          <el-button
            class="actions-button"
            type="text"
            size="small"
            :disabled="scope['row']['is_current_user']"
            @click="showResetPassword([scope['row']['id']])"
          >
            重置密码
          </el-button>
          <el-button
            class="actions-button"
            :style="scope['row']['is_current_user'] ? '' : 'color: red'"
            type="text"
            size="small"
            :disabled="scope['row']['is_current_user']"
            @click="showDeleteDialog(scope['row'])"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      layout="total, sizes, prev, pager, next"
      :pager-count="5"
      :page-sizes="[10, 20, 50, 100]"
      :total="total"
      :page-size.sync="pageSize"
      :current-page="currentPage"
      @size-change="refreshData"
      @current-change="pullData"
    />
    <el-dialog
      ref="profile_dialog"
      width="600px"
      :title="profileData === null ? '添加用户' : '修改用户信息'"
      :visible.sync="profileDialogVisible"
    >
      <UserProfile
        v-if="!profileReset"
        ref="profile"
        :data="profileData"
        :user-type="activeTab"
        :action="profileData === null ? 'add' : 'edit'"
        @success="profileSuccess"
      />
    </el-dialog>
    <el-dialog
      ref="reset_password_dialog"
      width="480px"
      title="重置用户密码"
      :visible.sync="resetPasswordDialogVisible"
    >
      <UserPasswordReset
        v-if="!resetPasswordReset"
        ref="profile"
        :ids="resetPasswordIDs"
        @success="passwordResetSuccess"
        @cancel="resetPasswordDialogVisible = false"
      />
    </el-dialog>
  </el-main>
</template>

<script>
import '../../../plugins/element.js'
import axios from 'axios'
import UserProfile from "../components/UserProfile.vue";
import UserPasswordReset from "../components/UserPasswordReset.vue";

export default {
  name: 'Users',
  components: {
    UserProfile,
    UserPasswordReset
  },
  data() {
    return {
      activeTab: 'volunteer',
      tableData: [],
      currentPage: 1,
      pageSize: 10,
      total: 0,
      loading: false,
      cancel: null,
      profileDialogVisible: false,
      profileReset: false,
      profileData: null,
      profileAction: 'add',
      resetPasswordDialogVisible: false,
      resetPasswordReset: false,
      resetPasswordIDs: [],
      tableSelection: []
    }
  },
  computed: {
    userType() {
      return {student: '学生', school: '学校', volunteer: '志愿者'}[this.activeTab]
    },
    displayNameLabel() {
      return {student: '姓名', school: '名称', volunteer: '名字'}[this.activeTab]
    }
  },
  mounted() {
    this.refreshData()
  },
  methods: {
    resetPasswords() {
      let ids = []
      this.tableSelection.forEach((val) => {
        ids.push(val.id)
      })
      this.resetPasswordIDs = ids
      this.resetPasswordDialogVisible = true
      this.resetPasswordReset = true
      this.$nextTick(() => {
        this.resetPasswordReset = false
      })
    },
    rowSelectable(row) {
      return !row['is_current_user']
    },
    showProfile(data) {
      this.profileData = data
      this.profileDialogVisible = true
      this.profileReset = true
      this.$nextTick(() => {
        this.profileReset = false
      })
    },
    profileSuccess(refresh) {
      this.profileDialogVisible = false
      this.pullData()
      if (refresh) {
        this.$store.dispatch('updateUserInfo')
      }
    },
    showResetPassword(ids) {
      this.resetPasswordIDs = ids
      this.resetPasswordDialogVisible = true
      this.resetPasswordReset = true
      this.$nextTick(() => {
        this.resetPasswordReset = false
      })
    },
    showDeleteDialog(row) {
      this.$confirm(`此操作将永久删除用户“${row['username']}”，是否继续？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$axios.delete(`/user/${row['id']}`).then(() => {
          this.$message.success('用户已删除!')
          this.pullData()
        }).catch(() => {
          this.$message.error('用户删除失败，请检查网络后重试')
        })
      })
    },
    passwordResetSuccess() {
      this.resetPasswordDialogVisible = false
      this.pullData()
    },
    handleSelection(val) {
      this.tableSelection = val
    },
    refreshData() {
      this.tableData = []
      this.currentPage = 1
      this.total = 0
      this.pullData()
    },
    pullData() {
      this.loading = true
      if (this.cancel !== null) {
        this.cancel()
      }
      this.$axios.get(`/users/${this.activeTab}`, {
        cancelToken: new axios.CancelToken((c) => {
          this.cancel = c
        }),
        params: {
          offset: (this.currentPage - 1) * this.pageSize,
          limit: this.pageSize
        }
      }).then((response) => {
        this.total = response.data['count']
        this.tableData = response.data['results']
      }).catch((error) => {
        if (!axios.isCancel(error)) {
          this.tableData = []
          this.total = 0
          this.$message.error('无法连接到服务器，请检查网络后重试！')
        }
      }).then(() => {
        this.cancel = null
        this.loading = false
      })
    }
  }
}
</script>

<style scoped>
  .actions-button {
    margin-top: -12px;
    margin-bottom: -12px;
    padding: 9px;
  }

  .gender-icon {
    position: relative;
    top: 1px;
    margin-left: 0.5em;
  }

  .cell-icon {
    position: relative;
    top: 1px;
    margin-left: 0.5em;
    cursor: pointer;
  }
</style>