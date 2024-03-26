

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(on b d)
(on c b)
(on d a)
(ontable e)
(clear c)
)
(:goal
(and
(on a c)
(on b e))
)
)


