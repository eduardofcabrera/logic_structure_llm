

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(on b d)
(ontable c)
(on d c)
(ontable e)
(clear a)
(clear b)
)
(:goal
(and
(on b e))
)
)


