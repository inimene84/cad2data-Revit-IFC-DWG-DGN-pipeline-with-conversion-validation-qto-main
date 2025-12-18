from typing import List, Dict, Any
import logging
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)

def process_excel_sheet(df: pd.DataFrame, sheet_name: str) -> Dict[str, Any]:
    """Process a single Excel sheet to find construction data"""
    column_mapping = {}
    construction_items = []
    
    try:
        # FIRST: Check if this is CAD export data
        cad_columns = ['Handle', 'ParentID', 'Color', 'Linetype', 'Lineweight']
        has_cad_data = sum(1 for col in cad_columns if col in df.columns) >= 3
        
        if has_cad_data and 'Name' in df.columns:
            column_mapping['material'] = 'Name'
            if 'Area' in df.columns: column_mapping['area'] = 'Area'
            if 'Length' in df.columns: column_mapping['length'] = 'Length'
            if 'Perimeter' in df.columns: column_mapping['perimeter'] = 'Perimeter'
            if 'Radius' in df.columns: column_mapping['radius'] = 'Radius'
            logger.info(f"Detected CAD export format in {sheet_name}")
        else:
            # Standard Excel search
            for col in df.columns:
                col_str = str(col).lower()
                if 'material' in col_str or 'item' in col_str or 'element' in col_str or 'materjal' in col_str or 'kirjeldus' in col_str or 'nimetus' in col_str:
                    if 'material' not in column_mapping: column_mapping['material'] = col
                if 'description' in col_str and 'material' not in column_mapping:
                    column_mapping['material'] = col
                if 'quantity' in col_str or 'amount' in col_str or 'qty' in col_str or 'count' in col_str or 'kogus' in col_str or 'maht' in col_str:
                    column_mapping['quantity'] = col
                if col_str == 'unit' or 'ühik' in col_str or 'mõõt' in col_str:
                    column_mapping['unit'] = col
                if 'price' in col_str or 'cost' in col_str or 'hind' in col_str or 'maksumus' in col_str:
                    column_mapping['price'] = col

        if 'material' in column_mapping:
            for _, row in df.iterrows():
                material = row[column_mapping['material']]
                if pd.isna(material) or str(material).strip() == "": continue
                
                # Helper for safe float conversion
                def safe_float(val):
                    try:
                        if val is not None and not pd.isna(val): return float(val)
                    except (ValueError, TypeError): pass
                    return None

                quantity = safe_float(row.get(column_mapping.get('quantity'))) or 0.0
                price = safe_float(row.get(column_mapping.get('price'))) or 0.0
                area = safe_float(row.get(column_mapping.get('area')))
                length = safe_float(row.get(column_mapping.get('length')))
                perimeter = safe_float(row.get(column_mapping.get('perimeter')))
                radius = safe_float(row.get(column_mapping.get('radius')))

                item = {
                    'material': str(material),
                    'quantity': quantity,
                    'unit': str(row.get(column_mapping.get('unit'), 'unit')),
                    'price': price,
                    'sheet': sheet_name
                }
                
                if area is not None: item['area'] = round(area, 2)
                if length is not None: item['length'] = round(length, 2)
                if perimeter is not None: item['perimeter'] = round(perimeter, 2)
                if radius is not None: item['radius'] = round(radius, 2)
                
                construction_items.append(item)
                
        # Preview data
        df_preview = df.head(10).astype(str).where(pd.notnull(df), None)
        sheet_data = {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "construction_columns": list(column_mapping.values()),
            "sample_data": df_preview.to_dict('records')
        }
        
        return {
            "sheet_data": sheet_data,
            "construction_items": construction_items
        }
        
    except Exception as e:
        logger.warning(f"Error processing sheet {sheet_name}: {e}")
        return {"error": str(e)}

def deduplicate_cad_items(construction_items: List[Dict]) -> List[Dict]:
    """Deduplicate CAD items and aggregate quantities"""
    if not construction_items:
        return []

    # Check heuristics for CAD data
    total_qty_zero = sum(1 for item in construction_items if item.get('quantity', 0) == 0)
    is_cad_data = total_qty_zero > len(construction_items) * 0.8
    
    if not is_cad_data:
        return construction_items

    logger.info(f"Detected CAD layer data, deduplicating {len(construction_items)} items")
    material_counts = {}
    
    for item in construction_items:
        mat_name = item['material']
        # Cleanup logic
        clean_name = mat_name.replace('New_', '').replace('_Pen_No_', ' ').strip()
        if '__' in clean_name: clean_name = clean_name.split('__')[0]
        clean_name = clean_name.strip('_ ')
        
        if clean_name:
            if clean_name not in material_counts:
                material_counts[clean_name] = {
                    'material': clean_name, 'quantity': 0, 'unit': 'item', 'price': 0.0,
                    'sheet': item['sheet'], 'total_area': 0.0, 'total_length': 0.0,
                    'total_perimeter': 0.0, 'element_count': 0
                }
            
            data = material_counts[clean_name]
            data['quantity'] += 1
            data['element_count'] += 1
            if 'area' in item: data['total_area'] += item['area']
            if 'length' in item: data['total_length'] += item['length']
            if 'perimeter' in item: data['total_perimeter'] += item['perimeter']

    final_items = []
    for name, data in material_counts.items():
        item = {'material': name, 'sheet': data['sheet'], 'price': 0.0}
        
        # Categorization and pricing defaults
        name_lower = name.lower()
        if any(k in name_lower for k in ['wall', 'sein']):
            category, price_per_m2 = 'walls', 85.0
        elif any(k in name_lower for k in ['floor', 'põrand']):
            category, price_per_m2 = 'floors', 65.0
        elif any(k in name_lower for k in ['roof', 'katus']):
            category, price_per_m2 = 'roofing', 95.0
        elif any(k in name_lower for k in ['door', 'uks']):
            category, price_per_item = 'doors', 450.0
        elif any(k in name_lower for k in ['window', 'aken']):
            category, price_per_item = 'windows', 380.0
        elif any(k in name_lower for k in ['pipe', 'toru']):
            category, price_per_m = 'piping', 45.0
        elif any(k in name_lower for k in ['wire', 'kaabel', 'elekter']):
            category, price_per_m = 'electrical', 25.0
        elif any(k in name_lower for k in ['fill', 'täide']):
            category, price_per_m2 = 'areas', 15.0
        else:
            category, price_per_m2 = 'general', 25.0

        # Smart unit selection
        if data['total_area'] > 0:
            item['quantity'] = round(data['total_area'] / 1000000, 2)
            item['unit'] = 'm²'
            unit_price = locals().get('price_per_m2', 25.0)
        elif data['total_length'] > 0:
            item['quantity'] = round(data['total_length'] / 1000, 2)
            item['unit'] = 'm'
            unit_price = locals().get('price_per_m', 35.0)
        else:
            item['quantity'] = data['element_count']
            item['unit'] = 'item'
            unit_price = locals().get('price_per_item', 50.0)

        item['price'] = round(item['quantity'] * unit_price, 2)
        item['element_count'] = data['element_count']
        item['category'] = category
        final_items.append(item)

    return final_items
