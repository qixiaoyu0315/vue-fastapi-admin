<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives } from 'vue'
import {
  NButton,
  NForm,
  NFormItem,
  NInput,
  NSwitch,
  NTag,
  NInputNumber,
  NDatePicker,
  NPopconfirm,
  NLayout,
  NLayoutContent,
} from 'naive-ui'

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'

import { formatDate, renderIcon } from '@/utils'
import { useCRUD } from '@/composables'
import api from '@/api'
import TheIcon from '@/components/icon/TheIcon.vue'
import { useUserStore } from '@/store'

defineOptions({ name: '猪场管理' })

const $table = ref(null)
const queryItems = ref({})
const vPermission = resolveDirective('permission')

const {
  modalVisible,
  modalTitle,
  modalAction,
  modalLoading,
  handleSave,
  modalForm,
  modalFormRef,
  handleEdit,
  handleDelete,
  handleAdd,
} = useCRUD({
  name: '猪场数据',
  initForm: {
    username: '',
    email: '',
    // 猪场管理字段初始值
    sow_number: null,
    ear_tag: null,
    pig_breed: null,
    backfat_thickness: null,
    parity: null,
    gestation_days: null,
    pen_number: null,
    feed_intake: null,
    feeder_number: null,
    predicted_feed: null,
    set_feed: null,
    actual_feed: null,
    start_time: null,
    end_time: null,
    set_feed_amount: null,
    current_feed_amount: null,
    last_feed_time: null,
    control_switch: false,
    feeder_status: null,
    date: null,
    feeding_status: null,
    feeding_date: null,
    is_normal: true,
    last_set_time: null,
    status: null
  },
  doCreate: api.createUser,
  doUpdate: api.updateUser,
  doDelete: api.deleteUser,
  refresh: () => $table.value?.handleSearch(),
})

onMounted(() => {
  $table.value?.handleSearch()
})

const columns = [
  {
    title: '用户',
    key: 'username',
    width: 60,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '母猪号',
    key: 'sow_number',
    width: 60,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '电子耳标号',
    key: 'ear_tag',
    width: 60,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '猪种',
    key: 'pig_breed',
    width: 60,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '背膘厚度',
    key: 'backfat_thickness',
    width: 60,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '胎次',
    key: 'parity',
    width: 40,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '妊娠天数',
    key: 'gestation_days',
    width: 60,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '栏号',
    key: 'pen_number',
    width: 50,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '采食量',
    key: 'feed_intake',
    width: 60,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '下料器号',
    key: 'feeder_number',
    width: 60,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '预测采食量',
    key: 'predicted_feed',
    width: 60,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '设置采食量',
    key: 'set_feed',
    width: 60,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '实际采食量',
    key: 'actual_feed',
    width: 60,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '下料器状态',
    key: 'feeder_status',
    width: 60,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '采食状态',
    key: 'feeding_status',
    width: 60,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '日期',
    key: 'date',
    width: 80,
    align: 'center',
    ellipsis: { tooltip: true },
    render(row) {
      return h(
        NButton,
        { size: 'small', type: 'text', ghost: true },
        {
          default: () => (row.date !== null ? formatDate(row.date) : null),
        }
      )
    },
  },
  {
    title: '设备状态',
    key: 'status',
    width: 60,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '操作',
    key: 'actions',
    width: 80,
    align: 'center',
    fixed: 'right',
    render(row) {
      return [
        withDirectives(
          h(
            NButton,
            {
              size: 'small',
              type: 'primary',
              style: 'margin-right: 8px;',
              onClick: () => {
                handleEdit(row)
              },
            },
            {
              default: () => '编辑',
              icon: renderIcon('material-symbols:edit', { size: 16 }),
            }
          ),
          [[vPermission, 'post/api/v1/user/update']]
        ),
      ]
    },
  },
]
</script>

<template>
  <NLayout has-sider wh-full>
    <NLayoutContent>
      <CommonPage show-footer title="猪场管理">
        <template #action>
          <NButton v-permission="'post/api/v1/user/create'" type="primary" @click="handleAdd">
            <TheIcon icon="material-symbols:add" :size="18" class="mr-5" />添加记录
          </NButton>
        </template>
        <!-- 表格 -->
        <CrudTable
          ref="$table"
          v-model:query-items="queryItems"
          :columns="columns"
          :get-data="api.getUserList"
        >
          <template #queryBar>
            <QueryBarItem label="用户名称" :label-width="70">
              <NInput
                v-model:value="queryItems.username"
                clearable
                type="text"
                placeholder="请输入用户名称"
                @keypress.enter="$table?.handleSearch()"
              />
            </QueryBarItem>
            <QueryBarItem label="母猪号" :label-width="50">
              <NInput
                v-model:value="queryItems.sow_number"
                clearable
                type="text"
                placeholder="请输入母猪号"
                @keypress.enter="$table?.handleSearch()"
              />
            </QueryBarItem>
            <QueryBarItem label="电子耳标号" :label-width="80">
              <NInput
                v-model:value="queryItems.ear_tag"
                clearable
                type="text"
                placeholder="请输入电子耳标号"
                @keypress.enter="$table?.handleSearch()"
              />
            </QueryBarItem>
            <QueryBarItem label="栏号" :label-width="40">
              <NInput
                v-model:value="queryItems.pen_number"
                clearable
                type="text"
                placeholder="请输入栏号"
                @keypress.enter="$table?.handleSearch()"
              />
            </QueryBarItem>
            <QueryBarItem label="下料器号" :label-width="70">
              <NInput
                v-model:value="queryItems.feeder_number"
                clearable
                type="text"
                placeholder="请输入下料器号"
                @keypress.enter="$table?.handleSearch()"
              />
            </QueryBarItem>
          </template>
        </CrudTable>

        <!-- 编辑弹窗 -->
        <CrudModal
          v-model:visible="modalVisible"
          :title="modalTitle"
          :loading="modalLoading"
          @save="handleSave"
        >
          <NForm
            ref="modalFormRef"
            label-placement="left"
            label-align="left"
            :label-width="80"
            :model="modalForm"
          >
            <NFormItem label="母猪号" path="sow_number">
              <NInput v-model:value="modalForm.sow_number" clearable placeholder="请输入母猪号" />
            </NFormItem>
            <NFormItem label="电子耳标号" path="ear_tag">
              <NInput v-model:value="modalForm.ear_tag" clearable placeholder="请输入电子耳标号" />
            </NFormItem>
            <NFormItem label="猪种" path="pig_breed">
              <NInput v-model:value="modalForm.pig_breed" clearable placeholder="请输入猪种" />
            </NFormItem>
            <NFormItem label="背膘厚度" path="backfat_thickness">
              <NInputNumber v-model:value="modalForm.backfat_thickness" clearable placeholder="请输入背膘厚度" />
            </NFormItem>
            <NFormItem label="胎次" path="parity">
              <NInputNumber v-model:value="modalForm.parity" clearable placeholder="请输入胎次" />
            </NFormItem>
            <NFormItem label="妊娠天数" path="gestation_days">
              <NInputNumber v-model:value="modalForm.gestation_days" clearable placeholder="请输入妊娠天数" />
            </NFormItem>
            <NFormItem label="栏号" path="pen_number">
              <NInput v-model:value="modalForm.pen_number" clearable placeholder="请输入栏号" />
            </NFormItem>
            <NFormItem label="采食量" path="feed_intake">
              <NInputNumber v-model:value="modalForm.feed_intake" clearable placeholder="请输入采食量" />
            </NFormItem>
            <NFormItem label="下料器号" path="feeder_number">
              <NInput v-model:value="modalForm.feeder_number" clearable placeholder="请输入下料器号" />
            </NFormItem>
            <NFormItem label="预测采食量" path="predicted_feed">
              <NInputNumber v-model:value="modalForm.predicted_feed" clearable placeholder="请输入预测采食量" />
            </NFormItem>
            <NFormItem label="设置采食量" path="set_feed">
              <NInputNumber v-model:value="modalForm.set_feed" clearable placeholder="请输入设置采食量" />
            </NFormItem>
            <NFormItem label="实际采食量" path="actual_feed">
              <NInputNumber v-model:value="modalForm.actual_feed" clearable placeholder="请输入实际采食量" />
            </NFormItem>
            <NFormItem label="开始时间" path="start_time">
              <NDatePicker v-model:value="modalForm.start_time" type="datetime" clearable />
            </NFormItem>
            <NFormItem label="结束时间" path="end_time">
              <NDatePicker v-model:value="modalForm.end_time" type="datetime" clearable />
            </NFormItem>
            <NFormItem label="设置饲料量" path="set_feed_amount">
              <NInputNumber v-model:value="modalForm.set_feed_amount" clearable placeholder="请输入设置饲料量" />
            </NFormItem>
            <NFormItem label="当前饲料量" path="current_feed_amount">
              <NInputNumber v-model:value="modalForm.current_feed_amount" clearable placeholder="请输入当前饲料量" />
            </NFormItem>
            <NFormItem label="上次下料时间" path="last_feed_time">
              <NDatePicker v-model:value="modalForm.last_feed_time" type="datetime" clearable />
            </NFormItem>
            <NFormItem label="控制开关" path="control_switch">
              <NSwitch v-model:value="modalForm.control_switch" />
            </NFormItem>
            <NFormItem label="下料器状态" path="feeder_status">
              <NInput v-model:value="modalForm.feeder_status" clearable placeholder="请输入下料器状态" />
            </NFormItem>
            <NFormItem label="日期" path="date">
              <NDatePicker v-model:value="modalForm.date" type="date" clearable />
            </NFormItem>
            <NFormItem label="采食状态" path="feeding_status">
              <NInput v-model:value="modalForm.feeding_status" clearable placeholder="请输入采食状态" />
            </NFormItem>
            <NFormItem label="采食日期" path="feeding_date">
              <NDatePicker v-model:value="modalForm.feeding_date" type="date" clearable />
            </NFormItem>
            <NFormItem label="正常" path="is_normal">
              <NSwitch v-model:value="modalForm.is_normal" />
            </NFormItem>
            <NFormItem label="上次设置时间" path="last_set_time">
              <NDatePicker v-model:value="modalForm.last_set_time" type="datetime" clearable />
            </NFormItem>
            <NFormItem label="状态" path="status">
              <NInput v-model:value="modalForm.status" clearable placeholder="请输入状态" />
            </NFormItem>
          </NForm>
        </CrudModal>
      </CommonPage>
    </NLayoutContent>
  </NLayout>
</template> 