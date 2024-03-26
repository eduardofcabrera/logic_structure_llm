

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(on b e)
(ontable c)
(ontable d)
(on e a)
(clear b)
(clear d)
)
(:goal
(and
(on a b)
(on b c)
(on d e))
)
)


