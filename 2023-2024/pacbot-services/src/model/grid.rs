/// Enum for grid cell values.
#[derive(Clone, Copy, Debug, Eq, PartialEq, IntoPrimitive, TryFromPrimitive)]
#[repr(u8)]
#[allow(non_camel_case_types)]
pub enum GridValue {
    /// Wall
    I = 1,
    /// Normal pellet
    o = 2,
    /// Empty space
    e = 3,
    /// Power pellet
    O = 4,
    /// Ghost chambers
    n = 5,
    /// Cherry position
    c = 6,
}

/// Represents a Pacman grid. Locations can be represented as [GridPoint] or [GridPose].
/// <pre>
/// grid access = grid[y][x]
///
///                      north -y    angle=pi/2 <---\
///        grid[0][0] grid[0][1] grid[0][2]         \
///  west  grid[1][0] grid[1][1] grid[1][2]  east angle=0
///   -x   grid[2][0] grid[2][1] grid[2][2]   +x    /
///                      south +y   angle=-pi/2 <---/
/// </pre>
type Grid = Vec<Vec<GridValue>>;

/// Describes a position in a [Grid]. See [Point] for float version.
///
/// [GridPoint] = (x, y)
///
/// -y = north/up
///
/// +x = east/right
type GridPoint = (usize, usize);

/// Describes a position and angle in a [Grid]. See [Pose] for float version.
///
/// [GridPose] = ([GridPoint], angle)
///
/// +angle = counterclockwise
type GridPose = (GridPoint, f32);

/// Describes a position. See [GridPoint] for integer/grid version.
/// Integer values should represent the center of the corresponding grid cell.
///
/// [Point] = (x, y)
///
/// -y = north/up
///
/// +x = east/right
///
/// <pre>
/// 0-----------0-----------
/// | 1---------1-----------
/// | | 2    (walkable)
/// | |   3-----3-----------
/// | |   | 4---4-----------
/// | |   | | 5  (walkable)
/// 0 1   3 4   6-----------
/// | |   | |   |
///
///  012345678
/// 00////////
/// 1/1///////
/// 2//
/// 3// 3/////
/// 4// /4////
/// 5// //
/// 6// // 6//
/// 7// // /
/// 8// // /
/// </pre>
type Point = (f32, f32);

/// Describes a position and angle. See [GridPose] for integer/grid version.
///
/// [Pose] = ([Point], angle)
///
/// angle 0 = to the right or +x
/// +angle = counterclockwise
type Pose = (Point, f32);
