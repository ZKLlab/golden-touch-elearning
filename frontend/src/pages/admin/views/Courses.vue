<template>
  <el-main>
    <el-button
      type="primary"
      size="small"
      @click="createDialogVisible = true"
    >
      <font-awesome-icon icon="plus" />
      创建课程
    </el-button>
    <el-table>
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
      />
      <el-table-column
        prop="name"
        label="课程列表"
      >
        <template v-slot="scope">
          {{ scope['row']['name'] }} | {{ scope['row']['abbr'] }}<br>
          <small>{{ scope['row']['slug'] }}</small>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog
      title="创建课程"
      :visible.sync="createDialogVisible"
    >
      <CourseCreate />
    </el-dialog>
  </el-main>
</template>

<script>
import axios from 'axios'
import CourseCreate from "../components/CourseCreate";

export default {
  name: 'Courses',
  components: {
    CourseCreate
  },
  data() {
    return {
      tableData: [],
      currentPage: 1,
      pageSize: 10,
      total: 0,
      loading: false,
      cancel: null,
      createDialogVisible: false
    }
  },
  mounted() {
    this.refreshData()
  },
  methods: {
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
      this.$axios.get(`/courses`, {
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

</style>