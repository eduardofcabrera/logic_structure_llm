

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(on b c)
(ontable c)
(ontable d)
(ontable e)
(clear a)
(clear b)
(clear d)
)
(:goal
(and
(on a c)
(on d b)
(on e a))
)
)


