<template>
  <el-main>
    <div>
      <el-button
        type="primary"
        size="small"
        @click="showCreateCourseDialog"
      >
        <font-awesome-icon icon="book-medical" />
        创建课程
      </el-button>
      <el-button
        size="small"
        plain
        :disabled="loading"
        @click="pullData"
      >
        <font-awesome-icon
          icon="sync-alt"
          :spin="loading"
        />
        刷新
      </el-button>
    </div>
    <el-table
      v-loading="loading"
      :data="tableData"
      style="margin-top: 5px"
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
        type="index"
        label="#"
        width="40"
      />
      <el-table-column
        label="课程列表"
      >
        <template v-slot="scope">
          {{ scope['row']['name'] }}
          <template v-if="scope['row']['name'] !== scope['row']['abbr']">
            <el-divider direction="vertical" />
            {{ scope['row']['abbr'] }}
          </template>
          <br>
          <small>{{ scope['row']['slug'] }}</small>
        </template>
      </el-table-column>
      <el-table-column
        width="80"
        prop="lessons_count"
        label="课时数"
      />
      <el-table-column
        label="类别"
      >
        <template v-slot="scope">
          <el-tag>{{ scope['row']['category']['name'] }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="对外可见性"
        width="120"
      >
        <template v-slot="scope">
          <span v-if="scope['row']['visible']">
            <font-awesome-icon icon="eye" />
            可见
          </span>
          <span v-else>
            <font-awesome-icon icon="eye-slash" />
            不可见
          </span>
        </template>
      </el-table-column>
      <el-table-column
        width="180"
      >
        <template v-slot="scope">
          <el-button
            size="small"
            @click="detail(scope['row']['slug'])"
          >
            详细信息
          </el-button>
          <el-button
            size="small"
            type="danger"
            @click="deleteCourse(scope['row']['slug'])"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog
      title="创建课程"
      :visible.sync="createDialogVisible"
    >
      <CourseCreate
        v-if="!createReset"
        @success="createCourseSuccess"
      />
    </el-dialog>
  </el-main>
</template>

<script>
import axios from 'axios'
import CourseCreate from '../components/CourseCreate';

export default {
  name: 'Courses',
  components: {
    CourseCreate,
  },
  data() {
    return {
      tableData: [],
      loading: false,
      cancel: null,
      createDialogVisible: false,
      createReset: false,
    }
  },
  mounted() {
    this.refreshData()
  },
  methods: {
    refreshData() {
      this.tableData = []
      this.pullData()
    },
    pullData() {
      this.loading = true
      if (this.cancel !== null) {
        this.cancel()
        this.cancel = null
      }
      this.$axios.get(`/courses`, {
        cancelToken: new axios.CancelToken((c) => {
          this.cancel = c
        }),
      }).then((response) => {
        this.tableData = response.data
      }).catch((error) => {
        if (!axios.isCancel(error)) {
          this.tableData = []
          this.$message.error('无法连接到服务器，请检查网络后重试！')
        }
      }).then(() => {
        this.cancel = null
        this.loading = false
      })
    },
    detail(slug) {
      this.$router.push(`/courses/${slug}`)
    },
    showCreateCourseDialog() {
      this.createReset = true
      this.$nextTick(() => {
        this.createReset = false
        this.createDialogVisible = true
      })
    },
    createCourseSuccess(slug) {
      this.createDialogVisible = false
      this.detail(slug)
    },
    deleteCourse(slug) {
      this.$confirm('此操作将永久删除该课程，是否继续？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.loading = true
        this.$axios.delete(`/course/${slug}`).then(() => {
          this.$message.success('成功删除课程！')
          this.pullData()
        }).catch(() => {
          this.$message.error('无法连接到服务器，请检查网络后重试！')
        }).then(() => {
          this.loading = false
        })
      })
    },
  },
}
</script>

<style scoped>

</style>