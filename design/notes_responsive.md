# Responsive Design Notes

## Breakpoints

### Mobile (320px - 768px)
- Single column layout
- Full-width components
- Reduced padding and spacing
- Stacked elements vertically
- Touch-friendly button sizes (min 44x44px)

### Tablet (768px - 1024px)
- Two-column layout where appropriate
- Medium padding and spacing
- Maintained readability

### Desktop (1024px+)
- Max-width container (1200px)
- Optimal spacing and padding
- Multi-column layouts where appropriate
- Hover states fully functional

## Component Responsive Behavior

### Header
- **Mobile**: Reduced font size, compact padding
- **Tablet**: Standard sizing
- **Desktop**: Full spacing and typography

### QueryBox
- **Mobile**: Full width, stacked submit button
- **Tablet**: Full width with side-by-side layout
- **Desktop**: Centered with optimal width

### ResultCard
- **Mobile**: Full width, reduced padding
- **Tablet**: Full width, standard padding
- **Desktop**: Centered with max-width

### ExamplesList
- **Mobile**: Single column, full-width chips
- **Tablet**: Two columns
- **Desktop**: Multiple columns, wrapped layout

### DisclaimerBanner
- **Mobile**: Compact text, smaller font
- **Tablet**: Standard text
- **Desktop**: Full text display

## Deviations from Figma

### Accepted Deviations
- None currently documented (to be updated after Figma inspection)

### Justifications
- TBD

## Testing Notes
- Test on real devices when possible
- Use browser DevTools for responsive testing
- Test touch interactions on mobile devices
- Verify text readability at all breakpoints

