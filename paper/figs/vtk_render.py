"""Clean product-style render of one STL with VTK (offscreen).  python paper/figs/vtk_render.py part.stl out.png [size]"""
import sys
import vtk


def render(stl, png, size=900, color=(0.55, 0.68, 0.86), azim=-50, elev=28):
    r = vtk.vtkSTLReader(); r.SetFileName(str(stl)); r.Update()
    norms = vtk.vtkPolyDataNormals(); norms.SetInputConnection(r.GetOutputPort()); norms.SetFeatureAngle(35); norms.SplittingOn()
    m = vtk.vtkPolyDataMapper(); m.SetInputConnection(norms.GetOutputPort())
    a = vtk.vtkActor(); a.SetMapper(m)
    p = a.GetProperty(); p.SetColor(*color); p.SetAmbient(0.28); p.SetDiffuse(0.72); p.SetSpecular(0.25); p.SetSpecularPower(30)
    edges = vtk.vtkFeatureEdges(); edges.SetInputConnection(r.GetOutputPort()); edges.BoundaryEdgesOn(); edges.FeatureEdgesOn()
    edges.SetFeatureAngle(35); edges.ManifoldEdgesOff(); edges.NonManifoldEdgesOff(); edges.ColoringOff()
    em = vtk.vtkPolyDataMapper(); em.SetInputConnection(edges.GetOutputPort())
    em.SetResolveCoincidentTopologyToPolygonOffset()
    ea = vtk.vtkActor(); ea.SetMapper(em); ea.GetProperty().SetColor(0.12, 0.16, 0.24); ea.GetProperty().SetLineWidth(1.6)
    ren = vtk.vtkRenderer(); ren.AddActor(a); ren.AddActor(ea)
    ren.SetBackground(1, 1, 1); ren.SetBackgroundAlpha(0.0)
    kit = vtk.vtkLightKit(); kit.SetKeyLightIntensity(0.95); kit.AddLightsToRenderer(ren)
    win = vtk.vtkRenderWindow(); win.SetOffScreenRendering(1); win.AddRenderer(ren); win.SetSize(size, size)
    win.SetAlphaBitPlanes(1); win.SetMultiSamples(8)
    cam = ren.GetActiveCamera(); cam.SetViewUp(0, 0, 1)
    b = r.GetOutput().GetBounds(); c = [(b[0] + b[1]) / 2, (b[2] + b[3]) / 2, (b[4] + b[5]) / 2]
    cam.SetFocalPoint(*c); cam.SetPosition(c[0] + 1, c[1], c[2]); cam.Azimuth(azim); cam.Elevation(elev); cam.OrthogonalizeViewUp()
    cam.ParallelProjectionOn(); ren.ResetCamera(); cam.SetParallelScale(cam.GetParallelScale() * 0.93)
    win.Render()
    w2i = vtk.vtkWindowToImageFilter(); w2i.SetInput(win); w2i.SetInputBufferTypeToRGBA(); w2i.ReadFrontBufferOff(); w2i.Update()
    wr = vtk.vtkPNGWriter(); wr.SetFileName(str(png)); wr.SetInputConnection(w2i.GetOutputPort()); wr.Write()


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 900)
