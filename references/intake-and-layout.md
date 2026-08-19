# Bijia intake and layout reference

## Current-job input schema

Collect these fields from the user's message and attachments.

### Project and materials

- `project_name`: exact project or event title.
- `items`: ordered list of `name`, `quantity`, `unit`, and optional `specification`.
- `image_sources`: source DOCX/PDF/folder/images and, when necessary, item-to-image mapping.
- `output_directory`: optional; otherwise use a clearly named task output folder.

### Quotations

- exactly three `quotes`, each with `company` and `target_total`;
- optional fixed unit prices or pricing constraints;
- `primary_company`: company used for the image-backed material quotation and normally the contract Party B;
- whether tax is included, only when the user or source explicitly states it.

### Contract

- `contract_template` path or attachment;
- Party A instruction, normally “retain from template”;
- Party B legal name;
- tax number;
- bank name;
- bank account;
- bank code/行号 when applicable;
- contract amount if it is not the primary quotation total;
- payment terms, service dates, invoice type, and signing date only when supplied or explicitly requested.

## Missing-information questions

Ask one consolidated question when possible. Typical groupings:

1. “请提供三家报价公司名称、各自目标总价，并注明哪一家作为主报价及合同乙方。”
2. “请提供物料项目、数量、单位，以及含参考图片的源文件；若图片无法明确对应，请补充对应关系。”
3. “请提供合同模板及乙方税号、开户行、银行账号、行号；付款方式或日期若需变更也请一并说明。”

Do not repeat questions for facts already visible in a reliable attachment. If only one or two fields are missing, ask only for those fields.

## Quote-plan JSON

Use this shape for the task-local validation file:

```json
{
  "project_name": "Current project title",
  "primary_company": "Current primary company",
  "items": [
    {"name": "Item A", "quantity": 10, "unit": "个"}
  ],
  "quotes": [
    {
      "company": "Company A",
      "target_total": "10000.00",
      "unit_prices": ["1000.00"]
    }
  ]
}
```

Represent monetary inputs as strings or numbers; the validator uses decimal arithmetic. `unit_prices` must follow the same order as `items`.

## Layout families for the three comparison quotations

Choose three visibly different families appropriate to content density.

### Corporate landscape

- A4 landscape.
- Compact badge or quotation label at left, project and company at right.
- Wide table with merged project-name span and a prominent total card near the top.

### Formal portrait

- A4 portrait.
- Centered title, company underneath, classic bordered table, total at the bottom.
- Restrained official-document styling.

### Split-panel portrait

- A4 portrait.
- Large title panel on the left or top-left; project and total occupy a separate right-hand panel.
- Table may use a different semantic column order, such as unit before quantity, while retaining all required fields.

### Letterhead landscape

- A4 landscape.
- Company letterhead and metadata block at top; total shown as a right-aligned summary strip.
- Minimal borders with horizontal rules instead of a full grid.

Do not use the same merged ranges, title placement, total placement, column widths, row heights, border system, and orientation across all three files. Fonts and colors may reinforce the differences but cannot be the only differences.

## File naming

Use clear Chinese names containing role/company/total when practical, for example:

- `比价单-<公司>-<总价>元.xlsx`
- `主报价清单-<公司>-<总价>元-含图片.xlsx`
- `合同-<项目简称>-<乙方>.docx`

Avoid ambiguous names such as `报价1.xlsx` unless the user explicitly requests them.
