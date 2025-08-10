export default function PrintCard({html}:{html:string}) {
  // In a next step, render server-side HTML or use a styled React card for printing
  return (
    <div className="print:block hidden">
      <div dangerouslySetInnerHTML={{__html: html}} />
    </div>
  )
}
