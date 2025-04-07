import streamlit as st
import pandas as pd
import math
from io import BytesIO

# 计算函数（保持不变）
def calculate_steel_quantity(components, density=7850, weight_unit='吨'):
    total_weight = 0
    details = []
    for comp in components:
        if comp['type'] in ['H型钢', '工字钢', 'T型钢']:
            area = 2 * (comp['flange_width'] / 1000) * (comp['flange_thickness'] / 1000) + \
                   (comp['web_thickness'] / 1000) * (comp['height'] / 1000 - 2 * (comp['flange_thickness'] / 1000))
        elif comp['type'] == '圆钢管':
            outer_radius = comp['diameter'] / 2000
            inner_radius = outer_radius - (comp['thickness'] / 1000)
            area = math.pi * (outer_radius**2 - inner_radius**2)
        elif comp['type'] == '方钢管':
            outer_area = (comp['side_length'] / 1000)**2
            inner_area = (comp['side_length'] / 1000 - 2 * (comp['thickness'] / 1000))**2
            area = outer_area - inner_area
        elif comp['type'] == '矩形钢管':
            outer_area = (comp['height'] / 1000) * (comp['width'] / 1000)
            inner_area = (comp['height'] / 1000 - 2 * (comp['thickness'] / 1000)) * \
                         (comp['width'] / 1000 - 2 * (comp['thickness'] / 1000))
            area = outer_area - inner_area
        elif comp['type'] == '角钢':
            area = (comp['side_length1'] / 1000) * (comp['thickness'] / 1000) + \
                   (comp['side_length2'] / 1000 - comp['thickness'] / 1000) * (comp['thickness'] / 1000)
        elif comp['type'] in ['槽钢', 'C型钢', 'Z型钢']:
            area = (comp['web_thickness'] / 1000) * (comp['height'] / 1000) + \
                   2 * (comp['flange_width'] / 1000) * (comp['thickness'] / 1000)
        elif comp['type'] == '焊接箱型构件':
            area = 2 * (comp['height'] / 1000) * (comp['flange_thickness'] / 1000) + \
                   2 * (comp['width'] / 1000 - 2 * (comp['flange_thickness'] / 1000)) * (comp['web_thickness'] / 1000)
        elif comp['type'] in ["节点板", "钢板"]:
            area = (comp['length']) * (comp['width'] / 1000)
            volume = area * (comp['thickness'] / 1000)
            weight = volume * density * comp['quantity'] * comp['loss_factor']
            if weight_unit == '吨':
                weight /= 1000
            total_weight += weight
            details.append({
                '构件类型': comp['type'], '长度(m)': comp['length'], 
                '数量': comp['quantity'], '重量调整系数': comp['loss_factor'], 
                f'重量({weight_unit})': weight
            })
            continue
        elif comp['type'] == '圆钢':
            area = math.pi * (comp['diameter'] / 2000)**2
        elif comp['type'] == '扁钢':
            area = (comp['width'] / 1000) * (comp['thickness'] / 1000)

        volume = area * comp['length']
        weight = volume * density * comp['quantity'] * comp['loss_factor']
        if weight_unit == '吨':
            weight /= 1000
        total_weight += weight
        details.append({
            '构件类型': comp['type'], '长度(m)': comp['length'], 
            '数量': comp['quantity'], '重量调整系数': comp['loss_factor'], 
            f'重量({weight_unit})': weight
        })
    return total_weight, details

# Streamlit界面
st.title("钢结构工程量计算器（全种类版）")

# 初始化构件列表
if 'components' not in st.session_state:
    st.session_state.components = []

# 全局设置
st.subheader("全局设置")
weight_unit = st.selectbox("重量单位", ['吨', 'kg'])

# 输入区
st.subheader("添加构件")
comp_type_options = ["H型钢", "工字钢", "圆钢管", "方钢管", "矩形钢管", "角钢", "槽钢", 
                     "T型钢", "C型钢", "Z型钢", "焊接箱型构件", "节点板", "钢板", "圆钢", "扁钢"]
comp_type = st.selectbox("构件类型", comp_type_options)

# 输入字段
quantity = st.number_input("数量", min_value=1, value=1, step=1)
length = st.number_input("长度 (m)", min_value=0.0, value=12.0, step=0.5)
loss_factor = st.number_input("重量调整系数（1.0表示无调整）", min_value=1.0, value=1.05, step=0.01)

# 根据构件类型显示输入字段
if comp_type in ["H型钢", "工字钢", "T型钢"]:
    height = st.number_input("截面高度 (mm)", min_value=0.0, value=300.0, step=10.0)
    flange_width = st.number_input("翼缘宽度 (mm)", min_value=0.0, value=200.0, step=10.0)
    flange_thickness = st.number_input("翼缘厚度 (mm)", min_value=0.0, value=10.0, step=0.1)
    web_thickness = st.number_input("腹板厚度 (mm)", min_value=0.0, value=8.0, step=0.1)
    comp_data = {'type': comp_type, 'length': length, 'height': height, 
                 'flange_width': flange_width, 'flange_thickness': flange_thickness, 
                 'web_thickness': web_thickness, 'quantity': quantity, 'loss_factor': loss_factor}
elif comp_type == "圆钢管":
    diameter = st.number_input("直径 (mm)", min_value=0.0, value=200.0, step=10.0)
    thickness = st.number_input("壁厚 (mm)", min_value=0.0, value=10.0, step=0.1)
    comp_data = {'type': comp_type, 'length': length, 'diameter': diameter, 
                 'thickness': thickness, 'quantity': quantity, 'loss_factor': loss_factor}
elif comp_type == "方钢管":
    side_length = st.number_input("边长 (mm)", min_value=0.0, value=200.0, step=10.0)
    thickness = st.number_input("壁厚 (mm)", min_value=0.0, value=10.0, step=0.1)
    comp_data = {'type': comp_type, 'length': length, 'side_length': side_length, 
                 'thickness': thickness, 'quantity': quantity, 'loss_factor': loss_factor}
elif comp_type == "矩形钢管":
    height = st.number_input("高度 (mm)", min_value=0.0, value=300.0, step=10.0)
    width = st.number_input("宽度 (mm)", min_value=0.0, value=200.0, step=10.0)
    thickness = st.number_input("壁厚 (mm)", min_value=0.0, value=10.0, step=0.1)
    comp_data = {'type': comp_type, 'length': length, 'height': height, 
                 'width': width, 'thickness': thickness, 'quantity': quantity, 'loss_factor': loss_factor}
elif comp_type == "角钢":
    side_length1 = st.number_input("边长1 (mm)", min_value=0.0, value=50.0, step=10.0)
    side_length2 = st.number_input("边长2 (mm)", min_value=0.0, value=50.0, step=10.0)
    thickness = st.number_input("厚度 (mm)", min_value=0.0, value=5.0, step=0.1)
    comp_data = {'type': comp_type, 'length': length, 'side_length1': side_length1, 
                 'side_length2': side_length2, 'thickness': thickness, 'quantity': quantity, 'loss_factor': loss_factor}
elif comp_type in ["槽钢", "C型钢", "Z型钢"]:
    height = st.number_input("高度 (mm)", min_value=0.0, value=200.0, step=10.0)
    flange_width = st.number_input("翼缘宽度 (mm)", min_value=0.0, value=100.0, step=10.0)
    web_thickness = st.number_input("腹板厚度 (mm)", min_value=0.0, value=8.0, step=0.1)
    thickness = st.number_input("翼缘厚度 (mm)", min_value=0.0, value=10.0, step=0.1)
    comp_data = {'type': comp_type, 'length': length, 'height': height, 
                 'flange_width': flange_width, 'web_thickness': web_thickness, 
                 'thickness': thickness, 'quantity': quantity, 'loss_factor': loss_factor}
elif comp_type == "焊接箱型构件":
    height = st.number_input("高度 (mm)", min_value=0.0, value=400.0, step=10.0)
    width = st.number_input("宽度 (mm)", min_value=0.0, value=300.0, step=10.0)
    web_thickness = st.number_input("腹板厚度 (mm)", min_value=0.0, value=12.0, step=0.1)
    flange_thickness = st.number_input("翼缘板厚度 (mm)", min_value=0.0, value=16.0, step=0.1)
    comp_data = {'type': comp_type, 'length': length, 'height': height, 
                 'width': width, 'web_thickness': web_thickness, 
                 'flange_thickness': flange_thickness, 'quantity': quantity, 'loss_factor': loss_factor}
elif comp_type in ["节点板", "钢板"]:
    width = st.number_input("宽度 (mm)", min_value=0.0, value=300.0, step=10.0)
    thickness = st.number_input("厚度 (mm)", min_value=0.0, value=10.0, step=0.1)
    comp_data = {'type': comp_type, 'length': length, 'width': width, 
                 'thickness': thickness, 'quantity': quantity, 'loss_factor': loss_factor}
elif comp_type == "圆钢":
    diameter = st.number_input("直径 (mm)", min_value=0.0, value=20.0, step=10.0)
    comp_data = {'type': comp_type, 'length': length, 'diameter': diameter, 
                 'quantity': quantity, 'loss_factor': loss_factor}
elif comp_type == "扁钢":
    width = st.number_input("宽度 (mm)", min_value=0.0, value=50.0, step=10.0)
    thickness = st.number_input("厚度 (mm)", min_value=0.0, value=10.0, step=0.1)
    comp_data = {'type': comp_type, 'length': length, 'width': width, 
                 'thickness': thickness, 'quantity': quantity, 'loss_factor': loss_factor}

# 添加构件按钮
if st.button("添加构件"):
    st.session_state.components.append(comp_data)
    st.success(f"已添加 {comp_type}")

# 显示已添加的构件（使用 st.data_editor 实现直接编辑）
if st.session_state.components:
    st.subheader("已添加构件")
    df = pd.DataFrame(st.session_state.components)
    
    column_mapping = {
        'type': '构件类型', 'length': '长度(m)', 'quantity': '数量', 'loss_factor': '重量调整系数',
        'height': '高度(mm)', 'width': '宽度(mm)', 'flange_width': '翼缘宽度(mm)', 
        'flange_thickness': '翼缘厚度(mm)', 'web_thickness': '腹板厚度(mm)', 
        'diameter': '直径(mm)', 'thickness': '厚度(mm)', 'side_length': '边长(mm)', 
        'side_length1': '边长1(mm)', 'side_length2': '边长2(mm)'
    }
    
    df_display = df.copy()
    for col in df.columns:
        if col in column_mapping:
            df_display = df_display.rename(columns={col: column_mapping[col]})
    
    # 使用 st.data_editor 实现直接编辑
    edited_df = st.data_editor(
        df_display,
        num_rows="dynamic",
        key="data_editor",
        use_container_width=True
    )
    
    # 同步编辑后的数据到 session_state
    st.session_state.components = edited_df.rename(columns={v: k for k, v in column_mapping.items()}).to_dict('records')
    
    # 优化删除功能：支持多选删除
    selected_rows = st.multiselect(
        "选择要删除的构件",
        options=range(len(df_display)),
        format_func=lambda x: f"构件 #{x}"
    )
    
    if st.button("删除选中构件"):
        if selected_rows:
            # 按降序删除，避免索引混乱
            for i in sorted(selected_rows, reverse=True):
                del st.session_state.components[i]
            st.success(f"已删除构件: {selected_rows}")
        else:
            st.warning("请先选择要删除的构件！")

# 计算与导出（保持不变）
if st.button("计算工程量"):
    if st.session_state.components:
        total_weight, details = calculate_steel_quantity(st.session_state.components, 
                                                        weight_unit=weight_unit)
        st.subheader("计算结果")
        st.write(f"总重量: {total_weight:.3f} {weight_unit}")
        
        export_details = []
        for i, comp in enumerate(st.session_state.components):
            detail = details[i].copy()
            if comp['type'] in ['H型钢', '工字钢', 'T型钢']:
                section_code = f"{comp['type'][0]}{'%.0f' % comp['height']}*{'%.0f' % comp['flange_width']}*{'%.1f' % comp['web_thickness']}*{'%.1f' % comp['flange_thickness']}"
                detail.update({'截面型号': section_code})
            elif comp['type'] == '圆钢管':
                section_code = f"Φ{'%.0f' % comp['diameter']}×{'%.1f' % comp['thickness']}"
                detail.update({'截面型号': section_code})
            elif comp['type'] == '方钢管':
                section_code = f"□{'%.0f' % comp['side_length']}×{'%.1f' % comp['thickness']}"
                detail.update({'截面型号': section_code})
            elif comp['type'] == '矩形钢管':
                section_code = f"□{'%.0f' % comp['height']}×{'%.0f' % comp['width']}×{'%.1f' % comp['thickness']}"
                detail.update({'截面型号': section_code})
            elif comp['type'] == '角钢':
                section_code = f"∠{'%.0f' % comp['side_length1']}×{'%.0f' % comp['side_length2']}×{'%.1f' % comp['thickness']}"
                detail.update({'截面型号': section_code})
            elif comp['type'] in ['槽钢', 'C型钢', 'Z型钢']:
                prefix = "C" if comp['type'] == '槽钢' else comp['type'][0]
                section_code = f"{prefix}{'%.0f' % comp['height']}×{'%.0f' % comp['flange_width']}×{'%.1f' % comp['web_thickness']}×{'%.1f' % comp['thickness']}"
                detail.update({'截面型号': section_code})
            elif comp['type'] == '焊接箱型构件':
                section_code = f"□{'%.0f' % comp['height']}×{'%.0f' % comp['width']}×{'%.1f' % comp['web_thickness']}×{'%.1f' % comp['flange_thickness']}"
                detail.update({'截面型号': section_code})
            elif comp['type'] in ['节点板', '钢板']:
                section_code = f"PL{'%.0f' % comp['width']}×{'%.1f' % comp['thickness']}"
                detail.update({'截面型号': section_code})
            elif comp['type'] == '圆钢':
                section_code = f"Φ{'%.0f' % comp['diameter']}"
                detail.update({'截面型号': section_code})
            elif comp['type'] == '扁钢':
                section_code = f"FB{'%.0f' % comp['width']}×{'%.1f' % comp['thickness']}"
                detail.update({'截面型号': section_code})
            export_details.append(detail)
        
        export_df = pd.DataFrame(export_details)
        result_df_with_section = pd.DataFrame(export_details)[['构件类型', '截面型号', '长度(m)', '数量', '重量调整系数', f'重量({weight_unit})']]
        st.table(result_df_with_section)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            result_df_with_section.to_excel(writer, sheet_name='工程量计算结果', index=False)
        excel_data = output.getvalue()
        st.download_button(
            label="下载结果为Excel",
            data=excel_data,
            file_name="steel_quantity_result.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("请先添加构件！")

# 清空按钮
if st.button("清空构件"):
    st.session_state.components = []
    st.success("已清空所有构件")