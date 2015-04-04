=====================================================
:mod:`procgame.dmd` --- Dot-Matrix Display
=====================================================

.. module:: procgame.dmd

Frame
-----

.. class:: Frame(width, height)

    DMD frame/bitmap.

    .. method:: ascii()

        Returns an ASCII representation of itself.

    .. method:: clear()

        Fills the entire buffer with black dots.

    .. method:: copy()

        Returns a copy of itself.

    .. staticmethod:: copy_rect(dst, dst_x, dst_y, src, src_x, src_y, width, height, op='copy')

        Copies dots from this instance to `dst`, another :class:`Frame`. The
        source rectangle has its origin at (`src_x`, `src_y`) and its size is
        `width` x `height`. It is copied to a rectangle in the `dst` buffer
        with its origin at (`dst_x`, `dst_y`).

        :meth:`copy_rect` will adjust the rectangle to fit within the
        bounds of the source buffer, and will only copy those dots that would
        be within the bounds at the destination. This allows negative (out of
        bounds) origins to be used for the developer’s convenience.

        The `op` parameter, or operation, describes how the dots are gathered
        and applied. The following are valid op parameter values (all are
        strings):

            ``copy``
                Copies dots from the source to the destination.

            ``add``
                Adds the value of the source dot to that of the destination
                dot. The result is capped at 15 (0xf).

            ``sub``
                Subtracts the value of the source dot from the destination dot.
                The result will have a minimum value of 0.

            ``blacksrc``
                Like copy, except it only copies the dot from source to
                destination if the destination dot is non-zero. This allows for
                primitive alpha channels.

    .. method:: fill_rect(x, y, width, height, value)
    
        Fills the rectangle in this buffer described by origin `x`, `y` with
        size `width` x `height` with dot value `value`.

    .. method:: get_dot(x, y)

        Returns the dot value at position `x`, `y`.

    .. method:: set_dot(x, y, value)

        Assigns the value of the dot at `x`, `y` to `value`.

    .. attribute:: height

        Height of the frame in dots.

    .. attribute:: width

        Width of the frame in dots.
