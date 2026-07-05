"""
海底地形三维重建Demo
"""
from Ocean_SubNav.hardware_adapt.multibeam_sonar_parser import MultibeamSonarParser
from Ocean_SubNav.noise_optimize.sonar_scatter_denoise import SonarScatterDenoise
from Ocean_SubNav.scene_constraint.seabed_terrain_constraint import SeabedTerrainConstraint
from Common_LSG.slice_rebuild import SectionRebuilder

def seabed_rebuild_pipeline(bathy_path, output_path):
    parser = MultibeamSonarParser()
    seabed_data = parser.load_bathymetry_data(bathy_path)
    
    denoiser = SonarScatterDenoise()
    denoised_stack = [denoiser.water_column_noise_suppress(s) for s in seabed_data.section_stack]
    
    constraint = SeabedTerrainConstraint()
    constrained_stack = [constraint.seabed_slope_constrain(s) for s in denoised_stack]
    
    rebuilder = SectionRebuilder()
    seabed_model = rebuilder.non_orthogonal_rebuild(constrained_stack, seabed_data.spacing)
    
    print("海底地形三维重建完成，支持水下潜航离线导航")
    return seabed_model

if __name__ == "__main__":
    seabed_rebuild_pipeline("./seabed_bathy.csv", "./output/seabed_model.stl")