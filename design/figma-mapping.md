# Figma Design Mapping

## Figma Link
See `figma-link.txt` for the Figma design URL.

## UI Screens and Routes

### Screens
1. **Home/Query Screen**
   - Main query input interface
   - Example questions display
   - Welcome message
   - Disclaimer banner

2. **Results Screen**
   - Answer display
   - Source link
   - Last updated information
   - Show source details toggle

3. **Error States**
   - PII detection error
   - No match found
   - Advice refusal message
   - Loading state

## Components to Implement

### Header
- **Purpose**: Site header with branding
- **Elements**: Logo, title, navigation (if any)
- **Layout**: Full width, fixed or static positioning
- **Spacing**: TBD from Figma
- **Typography**: TBD from Figma

### QueryBox
- **Purpose**: Main query input component
- **Elements**: 
  - Text input field
  - Submit button
  - Placeholder text
  - Example question chips/buttons
- **States**: Default, focus, error (PII), loading
- **Layout**: Centered, responsive width
- **Spacing**: TBD from Figma

### ExamplesList
- **Purpose**: Display example questions
- **Elements**: Clickable chips/buttons with example queries
- **Layout**: Grid or flex layout
- **Interaction**: Click to populate query box
- **Hover states**: TBD from Figma

### ResultCard
- **Purpose**: Display FAQ answer
- **Elements**:
  - Answer text (≤3 sentences)
  - Source link
  - Last updated date
  - Show source details toggle
- **Layout**: Card-based layout
- **States**: Default, loading skeleton, empty state
- **Spacing**: TBD from Figma

### SourceLink
- **Purpose**: Display and link to source
- **Elements**: URL text, external link icon
- **Interaction**: Opens in new tab
- **Hover states**: TBD from Figma

### DisclaimerBanner
- **Purpose**: Display compliance disclaimer
- **Elements**: Disclaimer text from `disclaimer.txt`
- **Layout**: Persistent banner (top or bottom)
- **Styling**: TBD from Figma
- **Dismissible**: TBD from Figma

### Footer
- **Purpose**: Site footer (if present in design)
- **Elements**: Links, copyright, etc.
- **Layout**: TBD from Figma

## Visual Design Tokens

### Colors
- **Primary**: TBD from Figma
- **Secondary**: TBD from Figma
- **Text**: TBD from Figma
- **Background**: TBD from Figma
- **Borders**: TBD from Figma
- **Errors**: TBD from Figma
- **Links**: TBD from Figma

### Typography
- **Font Family**: TBD from Figma
- **Font Sizes**: TBD from Figma
- **Font Weights**: TBD from Figma
- **Line Heights**: TBD from Figma
- **Letter Spacing**: TBD from Figma

### Spacing
- **Scale**: TBD from Figma (typically 4px or 8px base)
- **Margin**: TBD from Figma
- **Padding**: TBD from Figma
- **Gap**: TBD from Figma

### Border Radius
- **Small**: TBD from Figma
- **Medium**: TBD from Figma
- **Large**: TBD from Figma

### Shadows
- **Small**: TBD from Figma
- **Medium**: TBD from Figma
- **Large**: TBD from Figma

### Breakpoints
- **Mobile**: TBD from Figma (typically 320px-768px)
- **Tablet**: TBD from Figma (typically 768px-1024px)
- **Desktop**: TBD from Figma (typically 1024px+)

## Interaction Notes

### Hover States
- Buttons: TBD from Figma
- Links: TBD from Figma
- Example chips: TBD from Figma

### Focus States
- Input fields: TBD from Figma
- Buttons: TBD from Figma
- Links: TBD from Figma

### Transitions
- Duration: TBD from Figma
- Easing: TBD from Figma
- Properties: TBD from Figma

### Micro-animations
- Button hover effects: TBD from Figma
- Input focus animations: TBD from Figma
- Result card entrance: TBD from Figma
- Loading skeletons: TBD from Figma

## Assets

### Icons
- External link icon: TBD
- Submit/search icon: TBD
- Error icon: TBD
- Loading spinner: TBD

### Images
- Logo: TBD
- Placeholder images: TBD

### Usage Notes
- Asset sizes: TBD
- Formats: TBD (SVG preferred for icons)
- Optimization: TBD

## Notes
- This document will be updated as Figma design is inspected
- All measurements should be extracted from Figma
- Design tokens should match Figma specifications exactly
- Responsive behavior should match Figma breakpoints

