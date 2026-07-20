### Task 2: Implement Dynamic Width and Thousands Separator Formatter in PremiumPpmByFactorPlot

**Files:**
- Modify: `app/core/plot/components.py`

**Interfaces:**
- Consumes: `ncf_df_dict` inside `PremiumPpmByFactorPlot`
- Produces: Enhanced `go.Figure` with dynamic column widths and formatted texts

- [ ] **Step 1: Compute dynamic weights for subplot columns**
Modify `PremiumPpmByFactorPlot.render` to dynamically calculate the width weight for each subplot.
Before initializing `make_subplots`, iterate over `GROUPS` to determine each factor's data length, limit to `TOP_N`, and apply the minimum limit of `3`.

```python
            # X축 컬럼 수에 비례하는 동적 너비 가중치 계산 (하한값 3 보장)
            widths = []
            for dict_key, x_col, _ in GROUPS:
                df = self.ncf_df_dict.get(dict_key, pd.DataFrame())
                num_items = min(len(df), TOP_N) if not df.empty else 0
                widths.append(max(num_items, 3))
            
            total_width = sum(widths)
            normalized_widths = [w / total_width for w in widths]
```

- [ ] **Step 2: Inject dynamic column widths into subplot configuration**
Supply the computed `column_widths` to the `make_subplots` constructor.

```python
            fig = make_subplots(
                rows=1,
                cols=4,
                subplot_titles=[g[2] for g in GROUPS],
                shared_yaxes=False,
                horizontal_spacing=0.06,
                column_widths=normalized_widths  # 동적 너비 할당
            )
```

- [ ] **Step 3: Update text template to show thousands separator**
Inside the trace loop's `go.Bar` configuration, modify `texttemplate` to show formatted numbers.

```python
                fig.add_trace(
                    go.Bar(
                        x=df[x_col].astype(str),
                        y=df["PPM"],
                        text=df["PPM"].apply(lambda v: f"{v:,.0f}"),
                        textposition="outside",
                        texttemplate="%{y:,.0f}",  # 쉼표 구분 기호 표기 적용
                        textfont=dict(size=9, family=get_font_family("primary")),
                        marker_color=BAR_COLOR,
                        opacity=0.85,
                        customdata=df[["DFT_QTY", "count"]].values,
                        ...
                    ),
                    row=1,
                    col=col_idx,
                )
```

- [ ] **Step 4: Run static code verification**
Execute the static verifier to ensure no syntax errors, linting issues, or rule violations are introduced.
Run: `python tests/verify_code.py`
Expected: PASS

- [ ] **Step 5: Run unit tests**
Run existing unit tests to confirm that importing pages does not crash.
Run: `pytest tests/test_layer_boundary.py`
Expected: PASS
